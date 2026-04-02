# 💰 Real Estate Data Control Tower | Tour de Contrôle & Prévision Budgétaire

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cash-flow-forecast-portfolio-ofk.streamlit.app/)
![Prophet](https://img.shields.io/badge/Model-Facebook_Prophet-blue)
![Plotly](https://img.shields.io/badge/Viz-Plotly_Interactive-orange)

## 📉 Le Problème Business
Pour une PME, la trésorerie est le nerf de la guerre. Pourtant, beaucoup de dirigeants pilotent "au rétroviseur" (soldes passés) et découvrent les tensions de trésorerie (salaires, TVA, loyers) au dernier moment.

**La Solution :** Un outil de **Forecasting Financier** qui permet de :
1.  **Visualiser** la trésorerie future à 30/60/90 jours.
2.  **Détecter** automatiquement les cycles récurrents (ex: chute des salaires le 28 du mois).
3.  **Alerter** sur les risques de découvert avant qu'ils n'arrivent.

👉 **[Voir la démo interactive](https://cash-flow-forecast-portfolio-ofk.streamlit.app/)**

---

## 🧠 Intelligence Embarquée (Time Series)

L'outil utilise l'algorithme **Prophet** (développé par Meta) pour décomposer les flux financiers en trois composantes :
* **Trend (Tendance) :** L'entreprise est-elle en croissance ou décroissance structurelle ?
* **Saisonnalité Hebdomadaire :** Impact des week-ends sur les encaissements.
* **Saisonnalité Mensuelle :** Impact des décaissements fixes (Salaires, Loyer, Charges).

*Note : Les données présentées sont simulées pour reproduire le comportement comptable d'une agence digitale.*

---

## 🛠️ Stack Technique

* **Langage :** Python 3.10
* **Time Series Forecasting :** Prophet (Additive model).
* **Visualisation :** Plotly (Graphiques interactifs et zoomables).
* **App Web :** Streamlit.

---

## 👤 Auteur

**Oumar** - *Data Product Manager*
> J'aide les décideurs à transformer leurs données en outils de pilotage stratégique.

[LinkedIn](https://www.linkedin.com/in/oumarfodek/)
