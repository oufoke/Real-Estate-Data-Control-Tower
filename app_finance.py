import streamlit as st
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(page_title="Météo Trésorerie", layout="wide")

# --- TITRE & CONTEXTE ---
st.title("💰 Météo Trésorerie & Prévisionnel")
st.markdown("""
Cet outil permet d'anticiper les **tensions de trésorerie** à 30/60/90 jours.
Il utilise un modèle de série temporelle (Prophet) pour détecter les cycles (salaires, TVA, loyers).
""")

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    df = pd.read_csv('tresorerie.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# Affichage des KPIs actuels
last_date = df['Date'].iloc[-1]
last_solde = df['Solde'].iloc[-1]

col1, col2, col3 = st.columns(3)
col1.metric("Date du dernier relevé", last_date.strftime('%d/%m/%Y'))
col2.metric("Solde Actuel", f"{last_solde:,.2f} €")
col3.info("💡 Le modèle apprend sur 2 ans d'historique")

# --- PARAMÈTRES UTILISATEUR ---
st.sidebar.header("⚙️ Configuration Prévision")
horizon = st.sidebar.slider("Horizon de prévision (Jours)", 30, 180, 60)

# --- PRÉPARATION POUR PROPHET ---
# Prophet exige deux colonnes précises : 'ds' (date) et 'y' (valeur à prédire)
df_prophet = df[['Date', 'Solde']].rename(columns={'Date': 'ds', 'Solde': 'y'})

# --- ENTRAÎNEMENT DU MODÈLE ---
with st.spinner('Le modèle analyse les cycles financiers...'):
    # CORRECTION : On désactive le daily (inutile) et on ajoute manuellement le mensuel
    m = Prophet(daily_seasonality=False, weekly_seasonality=True, yearly_seasonality=True)
    
    # On force le modèle à chercher un motif qui se répète tous les 30.5 jours (Mois)
    m.add_seasonality(name='mensuel', period=30.5, fourier_order=5)
    
    m.fit(df_prophet)
    
    # Création du futur
    future = m.make_future_dataframe(periods=horizon)
    forecast = m.predict(future)

# --- VISUALISATION (PRODUIT) ---
st.subheader(f"🔮 Projection de Trésorerie à J+{horizon}")

# On utilise Plotly pour avoir un graph interactif (zoomable)
fig = plot_plotly(m, forecast)

# Personnalisation du graphique pour le rendre "Business"
fig.update_layout(
    title="Évolution historique et future",
    xaxis_title="Date",
    yaxis_title="Solde (€)",
    showlegend=False
)

# Ajout d'une ligne rouge "Seuil Critique" (0€)
fig.add_hline(y=0, line_dash="dot", line_color="red", annotation_text="DÉCOUVERT")

st.plotly_chart(fig, use_container_width=True)

# --- ANALYSE DE RISQUE (La valeur ajoutée DPM) ---
# On regarde la valeur prédite la plus basse dans le futur
min_future_cash = forecast.tail(horizon)['yhat_lower'].min()
date_min_cash = forecast.loc[forecast['yhat_lower'] == min_future_cash, 'ds'].iloc[0]

st.markdown("---")
st.subheader("⚠️ Analyse de Risque")

col_risk1, col_risk2 = st.columns(2)

with col_risk1:
    if min_future_cash < 0:
        st.error(f"🚨 ALERTE ROUGE : Risque de découvert détecté !")
        st.write(f"Le modèle prévoit un passage à **{min_future_cash:,.2f} €** autour du **{date_min_cash.strftime('%d/%m/%Y')}**.")
        st.write("👉 Conseil : Décalez les décaissements prévus cette semaine-là.")
    else:
        st.success(f"✅ Trésorerie saine sur la période.")
        st.write(f"Le point le plus bas sera de **{min_future_cash:,.2f} €** (Scénario pessimiste).")

with col_risk2:
    # Explication des composants (ce que Prophet a compris)
    st.info("Ce que le modèle a détecté :")
    st.markdown("""
    * **Tendance de fond :** L'entreprise gagne-t-elle de l'argent globalement ?
    * **Saisonnalité hebdo :** Moins d'encaissements le week-end.
    * **Saisonnalité mensuelle :** La chute brutale du 28 (Salaires) et du 1er (Loyer).
    """)