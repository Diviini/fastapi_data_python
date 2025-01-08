import matplotlib.pyplot as plt
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

# 1. Revenu par catégorie
fig, ax = plt.subplots()
categories = list(revenue_by_category.keys())
revenues = list(revenue_by_category.values())
ax.barh(categories, revenues, color="skyblue")
ax.set_title("Revenu par Catégorie")
ax.set_xlabel("Revenu (USD)")
st.pyplot(fig)

# 2. Revenu par saison
fig, ax = plt.subplots()
seasons = list(revenue_by_season.keys())
season_revenues = list(revenue_by_season.values())
ax.bar(seasons, season_revenues, color="lightgreen")
ax.set_title("Revenu par Saison")
ax.set_ylabel("Revenu (USD)")
st.pyplot(fig)

# 3. Meilleur article vendu par catégorie
# Meilleur article vendu par catégorie
best_selling_item_by_category = fetch_data("/kpi/best_selling_item_by_category")["best_selling_item_by_category"]

categories = list(best_selling_item_by_category.keys())
# Récupère le nom de l'article le plus vendu (le deuxième élément dans chaque liste)
best_selling_items = [item[1] for item in best_selling_item_by_category.values()]

fig, ax = plt.subplots()
ax.barh(categories, best_selling_items, color="coral")
ax.set_title("Meilleur Article Vendu par Catégorie")
ax.set_xlabel("Articles")
st.pyplot(fig)



# 4. Taux d'abonnés
fig, ax = plt.subplots()
ax.pie([subscription_percentage, 100 - subscription_percentage], labels=["Abonnés", "Non Abonnés"], autopct="%1.1f%%", colors=["#ff9999", "#66b3ff"])
ax.set_title("Taux d'Abonnés")
st.pyplot(fig)

# 5. Taux d'utilisation des codes promo
fig, ax = plt.subplots()
ax.pie([promo_code_usage_rate, 100 - promo_code_usage_rate], labels=["Utilisation Codes Promo", "Non Utilisé"], autopct="%1.1f%%", colors=["#ffcc99", "#99ff99"])
ax.set_title("Taux d'Utilisation des Codes Promo")
st.pyplot(fig)

# 6. Taux de clients fréquents
fig, ax = plt.subplots()
ax.pie([frequent_shopper_rate, 100 - frequent_shopper_rate], labels=["Clients Fréquents", "Autres Clients"], autopct="%1.1f%%", colors=["#c2c2f0", "#ffb3e6"])
ax.set_title("Taux de Clients Fréquents")
st.pyplot(fig)
