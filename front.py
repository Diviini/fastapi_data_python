import plotly.graph_objects as go
import requests
import streamlit as st
import pandas as pd

# Configuration de l'URL de l'API
API_URL = "http://127.0.0.1:8000"

# Titre de la page / Config
st.set_page_config(page_title="Customer Shopping Trends Dashboard", layout="wide")
st.title("Dashboard des Tendances d'Achat")
st.write("Ce tableau de bord présente les indicateurs clés de performance (KPI) et les graphiques analytiques pour mieux comprendre les tendances d'achat.")

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
st.write("Les KPIs suivants fournissent un aperçu rapide des performances globales des ventes et du comportement des clients.")

# Récupération des données pour chaque KPI
average_order_value = fetch_data("/kpi/average_order_value")["average_order_value"]
most_purchased_item = fetch_data("/kpi/most_purchased_item")["most_purchased_item"]
average_review_rating = fetch_data("/kpi/average_review_rating")["average_review_rating"]
subscription_percentage = fetch_data("/kpi/subscription_percentage")["subscription_percentage"]
promo_code_usage_rate = fetch_data("/kpi/promo_code_usage_rate")["promo_code_usage_rate"]
frequent_shopper_rate = fetch_data("/kpi/frequent_shopper_rate")["frequent_shopper_rate"]
revenue_by_category = fetch_data("/kpi/revenue_by_category")["revenue_by_category"]
revenue_by_season = fetch_data("/kpi/revenue_by_season")["revenue_by_season"]
best_selling_item_by_category = fetch_data("/kpi/best_selling_item_by_category")["best_selling_item_by_category"]
revenue_by_location = fetch_data("/kpi/revenue_by_location")["revenue_by_location"]
custumer_age_rate = fetch_data("/kpi/custumer_age_rate")["custumer_age_rate"]

# Affichage des KPIs sous forme de colonnes
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Article le Plus Acheté", most_purchased_item)
    st.metric("Taux de Clients Fréquents", f"{frequent_shopper_rate:.2f}%")

with col2:
    st.metric("Valeur Moyenne par Commande (USD)", f"${average_order_value:,.2f}")
    st.metric("Note Moyenne des Avis", f"{average_review_rating:.2f}")

with col3:
    st.metric("Pourcentage d'Abonnés", f"{subscription_percentage:.0f}%")
    st.metric("Taux d'Utilisation des Codes Promo", f"{promo_code_usage_rate:.0f}%")

# Graphiques
st.subheader("Graphiques")
st.write("Les graphiques suivants montrent la répartition des revenus, les comportements des clients et les articles les plus vendus.")

# Ajout de filtres généraux
st.sidebar.header("Filtres")
selected_category = st.sidebar.selectbox("Sélectionnez une catégorie", ["Toutes"] + list(revenue_by_category.keys()))
selected_season = st.sidebar.selectbox("Sélectionnez une saison", ["Toutes"] + list(revenue_by_season.keys()))
selected_location = st.sidebar.selectbox("Sélectionnez une location", ["Toutes"] + list(revenue_by_location.keys()))

# 1. Revenu par catégorie avec Plotly
if selected_category == "Toutes":
    categories = list(revenue_by_category.keys())
    revenues = list(revenue_by_category.values())
else:
    categories = [selected_category]
    revenues = [revenue_by_category[selected_category]]

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
if selected_season == "Toutes":
    seasons = list(revenue_by_season.keys())
    season_revenues = list(revenue_by_season.values())
else:
    seasons = [selected_season]
    season_revenues = [revenue_by_season[selected_season]]

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

# 3. Meilleur article vendu par catégorie sous forme de tableau
data = {
    "Catégorie": list(best_selling_item_by_category.keys()),
    "Meilleur Article": [item[1] for item in best_selling_item_by_category.values()]
}
df_best_selling = pd.DataFrame(data)

st.subheader("Meilleur Article Vendu par Catégorie")
st.table(df_best_selling)

# 4. Taux d'abonnés avec Plotly
st.write("Ce graphique montre la proportion des utilisateurs abonnés par rapport aux non-abonnés.")
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
st.write("Ce graphique illustre le taux d'utilisation des codes promotionnels lors des achats.")
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
st.write("Ce graphique montre la proportion des clients fréquents par rapport aux autres clients.")
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

# 7. Revenu par location avec Plotly
if selected_location == "Toutes":
    locations = list(revenue_by_location.keys())
    location_revenues = list(revenue_by_location.values())
else:
    locations = [selected_location]
    location_revenues = [revenue_by_location[selected_location]]

fig = go.Figure(go.Bar(
    x=locations,
    y=location_revenues,
    marker=dict(color='lightgreen')
))

fig.update_layout(
    title="Revenu par Location",
    xaxis_title="Location",
    yaxis_title="Revenu (USD)",
)

st.plotly_chart(fig)

# 8. Client par tranches d'âges
st.write("Ce graphique montre la répartition des clients par tranche d'âge.")
labels = list(custumer_age_rate.keys())
values = list(custumer_age_rate.values())

fig = go.Figure(go.Pie(
    labels=labels,
    values=values,
    hole=0.3
))

fig.update_layout(title="Taux de Clients par Tranche d'Âge")

st.plotly_chart(fig)
