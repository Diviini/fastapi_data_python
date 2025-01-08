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

#total_revenue = fetch_data("/kpi/total_revenue")["total_revenue"]
average_order_value = fetch_data("/kpi/average_order_value")["average_order_value"]
most_purchased_item = fetch_data("/kpi/most_purchased_item")["most_purchased_item"]
average_review_rating = fetch_data("/kpi/average_review_rating")["average_review_rating"]
subscription_percentage = fetch_data("/kpi/subscription_percentage")[
    "subscription_percentage"
]
promo_code_usage_rate = fetch_data("/kpi/promo_code_usage_rate")["promo_code_usage_rate"]
frequent_shopper_rate = fetch_data("/kpi/frequent_shopper_rate")["frequent_shopper_rate"]

# Affichage des KPIs
# st.metric("Revenu Total (USD)", f"${total_revenue:,.2f}")
st.metric("Valeur Moyenne par Commande (USD)", f"${average_order_value:,.2f}")
st.metric("Article le Plus Acheté", most_purchased_item)
st.metric("Note Moyenne des Avis", f"{average_review_rating:.2f}")
st.metric("Pourcentage d'Abonnés", f"{subscription_percentage:.2f}%")
st.metric("Taux d'Utilisation des Codes Promo", f"{promo_code_usage_rate:.2f}%")
st.metric("Taux de Clients Fréquents", f"{frequent_shopper_rate:.2f}%")

# Graphiques : Revenu par catégorie
st.subheader("Revenu par Catégorie")
revenue_by_category = fetch_data("/kpi/revenue_by_category")["revenue_by_category"]
categories = list(revenue_by_category.keys())
revenues = list(revenue_by_category.values())

fig, ax = plt.subplots()
ax.barh(categories, revenues, color="skyblue")
ax.set_title("Revenu par Catégorie")
ax.set_xlabel("Revenu (USD)")
st.pyplot(fig)
