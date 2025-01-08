import plotly.graph_objects as go
import requests
import streamlit as st

# Configuration de l'URL de l'API
API_URL = "http://127.0.0.1:8000"

# Titre de la page
st.title("Dashboard des Tendances d'Achat")

# Récupération des données depuis l'API
def fetch_data(endpoint):
    response = requests.get(f"{API_URL}{endpoint}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erreur lors de la récupération des données : {response.status_code}")
        return None


# KPIs principaux
st.subheader("Indicateurs Clés de Performance (KPI)")

# Récupération des données pour chaque KPI
total_revenue = fetch_data("/kpi/total_revenue")["total"]
average_order_value = fetch_data("/kpi/average_order_value")["average_order_value"]
most_purchased_item = fetch_data("/kpi/most_purchased_item")["most_purchased_item"]
average_review_rating = fetch_data("/kpi/average_review_rating")["average_review_rating"]
subscription_percentage = fetch_data("/kpi/subscription_percentage")["subscription_percentage"]
promo_code_usage_rate = fetch_data("/kpi/promo_code_usage_rate")["promo_code_usage_rate"]
frequent_shopper_rate = fetch_data("/kpi/frequent_shopper_rate")["frequent_shopper_rate"]
revenue_by_category = fetch_data("/kpi/revenue_by_category")["revenue_by_category"]
revenue_by_season = fetch_data("/kpi/revenue_by_season")["revenue_by_season"]
best_selling_item_by_category = fetch_data("/kpi/best_selling_item_by_category")["best_selling_item_by_category"]

# Affichage des KPIs sous forme de métriques
st.metric("Revenu Total (USD)", f"${float(total_revenue):,.2f}")
st.metric("Valeur Moyenne par Commande (USD)", f"${average_order_value:,.2f}")
st.metric("Article le Plus Acheté", most_purchased_item)
st.metric("Note Moyenne des Avis", f"{average_review_rating:.2f}")
st.metric("Pourcentage d'Abonnés", f"{subscription_percentage:.2f}%")
st.metric("Taux d'Utilisation des Codes Promo", f"{promo_code_usage_rate:.2f}%")
st.metric("Taux de Clients Fréquents", f"{frequent_shopper_rate:.2f}%")

# Graphiques
st.subheader("Graphiques")

# 1. Revenu par catégorie avec Plotly
categories = list(revenue_by_category.keys())
revenues = list(revenue_by_category.values())

fig = go.Figure(go.Bar(
    x=revenues,
    y=categories,
    orientation='h',
    marker=dict(color='skyblue')
))

fig.update_layout(
    title="Revenu par Catégorie",
    xaxis_title="Revenu (USD)",
    yaxis_title="Catégories",
)

st.plotly_chart(fig)

# 2. Revenu par saison avec Plotly
seasons = list(revenue_by_season.keys())
season_revenues = list(revenue_by_season.values())

fig = go.Figure(go.Bar(
    x=seasons,
    y=season_revenues,
    marker=dict(color='lightgreen')
))

fig.update_layout(
    title="Revenu par Saison",
    xaxis_title="Saison",
    yaxis_title="Revenu (USD)",
)

st.plotly_chart(fig)

# 3. Meilleur article vendu par catégorie avec Plotly
categories_best_selling = list(best_selling_item_by_category.keys())
best_selling_items = [item[1] for item in best_selling_item_by_category.values()]

fig = go.Figure(go.Bar(
    x=best_selling_items,
    y=categories_best_selling,
    orientation='h',
    marker=dict(color='coral')
))

fig.update_layout(
    title="Meilleur Article Vendu par Catégorie",
    xaxis_title="Articles",
    yaxis_title="Catégories",
)

st.plotly_chart(fig)

# 4. Taux d'abonnés avec Plotly
labels = ["Abonnés", "Non Abonnés"]
values = [subscription_percentage, 100 - subscription_percentage]

fig = go.Figure(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=["#ff9999", "#66b3ff"]),
    hole=0.3
))

fig.update_layout(title="Taux d'Abonnés")

st.plotly_chart(fig)

# 5. Taux d'utilisation des codes promo avec Plotly
labels = ["Utilisation Codes Promo", "Non Utilisé"]
values = [promo_code_usage_rate, 100 - promo_code_usage_rate]

fig = go.Figure(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=["#ffcc99", "#99ff99"]),
    hole=0.3
))

fig.update_layout(title="Taux d'Utilisation des Codes Promo")

st.plotly_chart(fig)

# 6. Taux de clients fréquents avec Plotly
labels = ["Clients Fréquents", "Autres Clients"]
values = [frequent_shopper_rate, 100 - frequent_shopper_rate]

fig = go.Figure(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=["#c2c2f0", "#ffb3e6"]),
    hole=0.3
))

fig.update_layout(title="Taux de Clients Fréquents")

st.plotly_chart(fig)
