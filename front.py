# -------------------------- FRONTEND (front.py) --------------------------
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Charger les données directement depuis le fichier CSV
data = pd.read_csv("data/shopping_trends.csv")
data.columns = data.columns.str.replace(' ', '_').str.lower()

# Nettoyage des données
data["subscription_status"] = data["subscription_status"].str.strip().str.lower()
data["promo_code_used"] = data["promo_code_used"].str.strip().str.lower()
data["frequency_of_purchases"] = data["frequency_of_purchases"].str.strip().str.lower()

# Fonction pour calculer le pourcentage d'abonnés
def calculate_subscription_percentage(df):
    abonnés = df[df["subscription_status"] == "yes"]
    return (len(abonnés) / len(df)) * 100

# Fonction pour calculer le taux d'utilisation des codes promo
def calculate_promo_code_usage(df):
    promo_utilisés = df[df["promo_code_used"] == "yes"]
    return (len(promo_utilisés) / len(df)) * 100

# Fonction pour calculer le taux de clients fréquents
def calculate_frequent_shopper_rate(df):
    fréquents = df[df["frequency_of_purchases"].isin(["weekly", "fortnightly"])]
    return (len(fréquents) / len(df)) * 100

# Dashboard interactif avec Streamlit
st.set_page_config(page_title="Dashboard des Tendances d'Achat")
st.title("Dashboard des Tendances d'Achat")
st.markdown("---")

# Section 1 : KPI Cards
st.header("Indicateurs Clés de Performance (KPI)")
col1, col2, col3 = st.columns(3)

# KPI 1 : Valeur moyenne par commande
col1.metric("Valeur Moyenne par Commande (USD)", f"${data['purchase_amount_(usd)'].mean():.2f}")

# KPI 2 : Article le plus acheté
col2.metric("Article le Plus Acheté", data['item_purchased'].value_counts().idxmax())

# KPI 3 : Note moyenne des avis
col3.metric("Note Moyenne des Avis", f"{data['review_rating'].mean():.2f}")

# KPI 4 : Pourcentage d'abonnés
col1.metric("Pourcentage d'Abonnés", f"{calculate_subscription_percentage(data):.2f}%")

# KPI 5 : Taux d'utilisation des codes promo
col2.metric("Taux d'Utilisation des Codes Promo", f"{calculate_promo_code_usage(data):.2f}%")

# KPI 6 : Taux de clients fréquents
col3.metric("Taux de Clients Fréquents", f"{calculate_frequent_shopper_rate(data):.2f}%")

st.markdown("---")

# Section 2 : Visualisations
st.header("Revenu par Catégorie")
fig, ax = plt.subplots(figsize=(10, 5))
category_revenue = data.groupby('category')['purchase_amount_(usd)'].sum()
ax.barh(category_revenue.index, category_revenue.values, color="skyblue")
ax.set_xlabel("Revenu (USD)")
ax.set_title("Revenu par Catégorie")
st.pyplot(fig)