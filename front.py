import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Charger les données localement
def load_data():
    # Remplacer cette ligne par un chemin vers le fichier CSV local si nécessaire
    data = pd.read_csv("data/shopping_trends.csv")
    return clean_data(data)

# Nettoyage des données
def clean_data(df):
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()
    df = df.dropna()
    colonnes_textes = [
        "gender", "category", "location", "season", "payment_method",
        "shipping_type", "discount_applied", "promo_code_used",
        "frequency_of_purchases", "subscription_status",
    ]
    for col in colonnes_textes:
        if col in df.columns:
            df[col] = df[col].str.strip().str.lower()
    if "purchase_amount_(usd)" in df.columns:
        df["purchase_amount_(usd)"] = pd.to_numeric(df["purchase_amount_(usd)"], errors="coerce")
    if "review_rating" in df.columns:
        df["review_rating"] = pd.to_numeric(df["review_rating"], errors="coerce")
    if "age" in df.columns:
        df = df[(df["age"] > 0) & (df["age"] < 100)]
    if "purchase_amount_(usd)" in df.columns:
        df = df[df["purchase_amount_(usd)"] > 0]
    return df

# Fonctions pour les KPI
def total_revenue(df):
    return df["purchase_amount_(usd)"].sum()

def average_order_value(df):
    return df["purchase_amount_(usd)"].mean()

def revenue_by_category(df):
    return df.groupby("category")["purchase_amount_(usd)"].sum().to_dict()

def most_purchased_item(df):
    return df["item_purchased"].value_counts().idxmax()

def average_review_rating(df):
    return df["review_rating"].mean()

def revenue_by_season(df):
    return df.groupby("season")["purchase_amount_(usd)"].sum().to_dict()

def subscription_percentage(df):
    abonnés = df[df["subscription_status"] == "yes"]
    return (len(abonnés) / len(df)) * 100

def promo_code_usage_rate(df):
    promo_utilisés = df[df["promo_code_used"] == "yes"]
    return (len(promo_utilisés) / len(df)) * 100

def frequent_shopper_rate(df):
    fréquents = df[df["frequency_of_purchases"].isin(["weekly", "fortnightly"])]
    return (len(fréquents) / len(df)) * 100

def best_selling_item_by_category(df):
    return df.groupby('category')['item_purchased'].value_counts().groupby('category').idxmax()

# Charger les données
data = load_data()

# KPIs principaux
st.title("Dashboard des Tendances d'Achat")
st.subheader("Indicateurs Clés de Performance (KPI)")

# Affichage des KPIs sous forme de métriques
st.metric("Revenu Total (USD)", f"${total_revenue(data):,.2f}")
st.metric("Valeur Moyenne par Commande (USD)", f"${average_order_value(data):,.2f}")
st.metric("Article le Plus Acheté", most_purchased_item(data))
st.metric("Note Moyenne des Avis", f"{average_review_rating(data):.2f}")
st.metric("Pourcentage d'Abonnés", f"{subscription_percentage(data):.2f}%")
st.metric("Taux d'Utilisation des Codes Promo", f"{promo_code_usage_rate(data):.2f}%")
st.metric("Taux de Clients Fréquents", f"{frequent_shopper_rate(data):.2f}%")

# Graphiques
st.subheader("Graphiques")

# 1. Revenu par catégorie
fig, ax = plt.subplots()
categories = list(revenue_by_category(data).keys())
revenues = list(revenue_by_category(data).values())
ax.barh(categories, revenues, color="skyblue")
ax.set_title("Revenu par Catégorie")
ax.set_xlabel("Revenu (USD)")
st.pyplot(fig)

# 2. Revenu par saison
fig, ax = plt.subplots()
seasons = list(revenue_by_season(data).keys())
season_revenues = list(revenue_by_season(data).values())
ax.bar(seasons, season_revenues, color="lightgreen")
ax.set_title("Revenu par Saison")
ax.set_ylabel("Revenu (USD)")
st.pyplot(fig)

# 3. Meilleur article vendu par catégorie
fig, ax = plt.subplots()
categories = list(best_selling_item_by_category(data).keys())
best_selling_items = [item[1] for item in best_selling_item_by_category(data).tolist()]
ax.barh(categories, best_selling_items, color="coral")
ax.set_title("Meilleur Article Vendu par Catégorie")
ax.set_xlabel("Articles")
st.pyplot(fig)

# 4. Taux d'abonnés
fig, ax = plt.subplots()
ax.pie([subscription_percentage(data), 100 - subscription_percentage(data)], labels=["Abonnés", "Non Abonnés"], autopct="%1.1f%%", colors=["#ff9999", "#66b3ff"])
ax.set_title("Taux d'Abonnés")
st.pyplot(fig)

# 5. Taux d'utilisation des codes promo
fig, ax = plt.subplots()
ax.pie([promo_code_usage_rate(data), 100 - promo_code_usage_rate(data)], labels=["Utilisation Codes Promo", "Non Utilisé"], autopct="%1.1f%%", colors=["#ffcc99", "#99ff99"])
ax.set_title("Taux d'Utilisation des Codes Promo")
st.pyplot(fig)

# 6. Taux de clients fréquents
fig, ax = plt.subplots()
ax.pie([frequent_shopper_rate(data), 100 - frequent_shopper_rate(data)], labels=["Clients Fréquents", "Autres Clients"], autopct="%1.1f%%", colors=["#c2c2f0", "#ffb3e6"])
ax.set_title("Taux de Clients Fréquents")
st.pyplot(fig)
