# Importation des bibliothèques nécessaires
import plotly.graph_objects as go   # Pour les graphiques interactifs
import requests                     # Pour effectuer des requêtes HTTP
import streamlit as st              # Pour créer l'interface utilisateur
import pandas as pd                 # Pour manipuler les données sous forme de DataFrame

# Configuration de l'URL de l'API
API_URL = "http://127.0.0.1:8000"

# Définition du titre de la page
st.title("Dashboard des Tendances d'Achat")
st.write("Ce tableau de bord présente les indicateurs clés de performance (KPI) et les graphiques analytiques pour mieux comprendre les tendances d'achat.")

# Fonction pour récupérer les données depuis l'API
def fetch_data(endpoint):
    response = requests.get(f"{API_URL}{endpoint}") # Effectue une requête GET à l'API
    if response.status_code == 200:                 # Vérifie si la requête a réussi
        return response.json()                      # Retourne les données JSON
    else:
        st.error(f"Erreur lors de la récupération des données : {response.status_code}")  # Affiche une erreur si la requête échoue
        return None

# Section pour les indicateurs clés de performance (KPIs)
st.subheader("Indicateurs Clés de Performance (KPI)")
st.write("Les KPIs suivants fournissent un aperçu rapide des performances globales des ventes et du comportement des clients.")

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
revenue_by_location = fetch_data("/kpi/revenue_by_location")["revenue_by_location"]
customer_age_rate = fetch_data("/kpi/customer_age_rate")["customer_age_rate"]
subscriber_frequent_relation_value = fetch_data("/kpi/subscriber_frequent_relation")["subscriber_frequent_relation"]

# Affichage des KPIs sous forme de colonnes
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Revenu Total (USD)", f"${float(total_revenue):,.0f}")
    st.metric("Article le Plus Acheté", most_purchased_item)
    st.metric("Taux de Clients Fréquents", f"{frequent_shopper_rate:.2f}%")
with col2:
    st.metric("Valeur Moyenne par Commande (USD)", f"${average_order_value:,.2f}")
    st.metric("Note Moyenne des Avis", f"{average_review_rating:.2f}")
with col3:
    st.metric("Pourcentage d'Abonnés", f"{subscription_percentage:.0f}%")
    st.metric("Taux d'Utilisation des Codes Promo", f"{promo_code_usage_rate:.0f}%")

# Tableau pour le meilleur article vendu par catégorie
data = {
    "Catégorie": list(best_selling_item_by_category.keys()),
    "Meilleur Article": [item[1] for item in best_selling_item_by_category.values()]
}
df_best_selling = pd.DataFrame(data)  # Conversion en DataFrame
st.subheader("Meilleur Article Vendu par Catégorie")
st.table(df_best_selling)

# Graphiques analytiques
st.subheader("Graphiques")
st.write("Les graphiques suivants montrent la répartition des revenus, les comportements des clients et les articles les plus vendus.")

# Graphique : Revenu par catégorie
categories = list(revenue_by_category.keys())
revenues = list(revenue_by_category.values())

# Trier les catégories et les revenus en fonction des revenus (décroissant)
sorted_categories, sorted_revenues = zip(*sorted(zip(categories, revenues), key=lambda x: x[1], reverse=True))

fig = go.Figure(go.Bar(
    x=sorted_revenues,
    y=sorted_categories,
    orientation='h',
    marker=dict(color='skyblue')
))

fig.update_layout(
    title="Revenu par Catégorie",
    xaxis_title="Revenu (USD)",
    yaxis_title="Catégories",
)

st.plotly_chart(fig)
st.write('Les revenus par catégorie peuvent aider à identifier les produits les plus populaires et à ajuster les stocks en conséquence.')

# Graphique : Revenu par saison
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
st.write('Les revenus par saison peuvent aider à identifier les périodes de l\'année où les ventes sont les plus élevées.')


# Graphique : Taux d'abonnés
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
st.write('Le taux d\'abonnés peut aider à évaluer la fidélité des clients et à concevoir des programmes de fidélisation.')


# Graphique : Taux d'utilisation des codes promo
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
st.write('Le taux d\'utilisation des codes promo peut aider à évaluer l\'efficacité des campagnes promotionnelles.')


# Graphique : Taux de clients fréquents
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
st.write('Les taux de clients fréquents peuvent aider à identifier les clients les plus fidèles et à concevoir des programmes de fidélisation.')


# Carte des revenus par État
states = list(revenue_by_location.keys())
revenues = list(revenue_by_location.values())
fig = go.Figure(data=go.Choropleth(
    locations=states,
    z=revenues,
    locationmode='USA-states',
    colorscale='YlGn',
    colorbar_title="Revenus ($)",
))
fig.update_layout(
    title_text='Carte des revenus par État',
    geo=dict(
        scope='usa',
        projection=go.layout.geo.Projection(type='albers usa'),
        showlakes=True,
        lakecolor='rgb(15, 17, 22)',
        bgcolor='rgb(15, 17, 22)'
    )
)
st.plotly_chart(fig)
st.write('La carte des revenus par État peut aider à identifier les régions où les ventes sont les plus élevées.')


# Graphique : Répartition des clients par tranche d'âge
labels = list(customer_age_rate.keys())
values = list(customer_age_rate.values())
fig = go.Figure(go.Pie(
    labels=labels,
    values=values,
    hole=0.3
))
fig.update_layout(title="Taux de clients par tranche d'âge")
st.plotly_chart(fig)
st.write('Savoir quels sont les tranches d\'âge les plus représentées parmi les clients peut aider à mieux cibler les campagnes marketing.')

