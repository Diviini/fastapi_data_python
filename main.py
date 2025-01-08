import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Charge les données
data = pd.read_csv('data/shopping_trends.csv')

# Nettoie les données
def clean_data(df):
    """
    Nettoie les données en résolvant les problèmes courants.
    """
    # Nettoyage des noms de colonnes
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()

    # Gestion des valeurs manquantes
    df = df.dropna()  # Supprime les lignes avec des valeurs manquantes

    # Standardisation des colonnes textuelles
    colonnes_textes = ['gender', 'category', 'location', 'season', 'payment_method',
                       'shipping_type', 'discount_applied', 'promo_code_used',
                       'frequency_of_purchases', 'subscription_status']
    for col in colonnes_textes:
        if col in df.columns:
            df[col] = df[col].str.strip().str.lower()

    # Conversion des colonnes numériques
    if 'purchase_amount_(usd)' in df.columns:
        df['purchase_amount_(usd)'] = pd.to_numeric(df['purchase_amount_(usd)'], errors='coerce')
    if 'review_rating' in df.columns:
        df['review_rating'] = pd.to_numeric(df['review_rating'], errors='coerce')

    # Gestion des valeurs aberrantes pour l'âge et le montant des achats
    if 'age' in df.columns:
        df = df[(df['age'] > 0) & (df['age'] < 100)]
    if 'purchase_amount_(usd)' in df.columns:
        df = df[df['purchase_amount_(usd)'] > 0]

    return df

data = clean_data(data)

# Fonctions pour les KPI
def total_revenue(df):
    """Calcule le revenu total."""
    return df['purchase_amount_(usd)'].sum()

def average_order_value(df):
    """Calcule la valeur moyenne d'une commande."""
    return df['purchase_amount_(usd)'].mean()

def revenue_by_category(df):
    """Calcule le revenu par catégorie."""
    return df.groupby('category')['purchase_amount_(usd)'].sum()

def most_purchased_item(df):
    """Identifie l'article le plus acheté."""
    return df['item_purchased'].value_counts().idxmax()

def average_review_rating(df):
    """Calcule la note moyenne des avis."""
    return df['review_rating'].mean()

def revenue_by_season(df):
    """Calcule le revenu par saison."""
    return df.groupby('season')['purchase_amount_(usd)'].sum()

def subscription_percentage(df):
    """Pourcentage de clients abonnés."""
    abonnés = df[df['subscription_status'] == 'yes']
    return (len(abonnés) / len(df)) * 100

def promo_code_usage_rate(df):
    """Taux d'utilisation des codes promo."""
    promo_utilisés = df[df['promo_code_used'] == 'yes']
    return (len(promo_utilisés) / len(df)) * 100

def frequent_shopper_rate(df):
    """Taux de clients fréquents."""
    fréquents = df[df['frequency_of_purchases'].isin(['weekly', 'fortnightly'])]
    return (len(fréquents) / len(df)) * 100

def revenue_by_location(df):
    """Calcule le revenu par localisation."""
    return df.groupby('location')['purchase_amount_(usd)'].sum()

# Interface Streamlit
st.title("Dashboard des Tendances d'Achat")

# Affiche les données nettoyées
st.subheader("Données Nettoyées")
st.dataframe(data)

# Affiche les KPIs principaux
st.subheader("Indicateurs Clés de Performance (KPI)")

st.metric("Revenu Total (USD)", f"${total_revenue(data):,.2f}")
st.metric("Valeur Moyenne par Commande (USD)", f"${average_order_value(data):,.2f}")
st.metric("Article le Plus Acheté", most_purchased_item(data))
st.metric("Note Moyenne des Avis", f"{average_review_rating(data):.2f}")
st.metric("Pourcentage d'Abonnés", f"{subscription_percentage(data):.2f}%")
st.metric("Taux d'Utilisation des Codes Promo", f"{promo_code_usage_rate(data):.2f}%")
st.metric("Taux de Clients Fréquents", f"{frequent_shopper_rate(data):.2f}%")

# Graphiques
st.subheader("Visualisation des Données")

# Revenu par Catégorie : Horizontal Bar Chart
st.subheader("Revenu par Catégorie")

fig, ax = plt.subplots()
categories = revenue_by_category(data).index
revenues = revenue_by_category(data).values

ax.barh(categories, revenues, color='skyblue')
ax.set_title("Revenu par Catégorie")
ax.set_xlabel("Revenu (USD)")
ax.set_ylabel("Catégories")

# Affiche le graphique
st.pyplot(fig)


# Revenu par Saison : Stacked Bar Chart
st.subheader("Revenu par Saison")

fig, ax = plt.subplots()
seasons = revenue_by_season(data).index
revenues = revenue_by_season(data).values

ax.bar(seasons, revenues, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
ax.set_title("Revenu par Saison")
ax.set_xlabel("Saisons")
ax.set_ylabel("Revenu (USD)")

# Affiche le graphique
st.pyplot(fig)


# Exemple des revenus par localisation (remplacez par vos données réelles)
revenue_loc = revenue_by_location(data)  # Revenue par localisation

# Chargement des données géographiques des États-Unis
us_map = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
us_states = us_map[us_map['iso_a2'] == 'US']

# Nettoyage des noms pour correspondre avec vos données
us_states['name'] = us_states['name'].str.lower()
revenue_loc.index = revenue_loc.index.str.lower()  # Assurez-vous que les noms correspondent

# Fusion des données
us_states = us_states.merge(revenue_loc, left_on='name', right_index=True, how='left')
us_states['revenue'] = us_states['purchase_amount']  # Ajustez au nom de votre colonne

# Création de la carte
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
us_states.plot(
    column='revenue',
    cmap='Blues',
    legend=True,
    legend_kwds={'label': "Revenu par État (USD)"},
    ax=ax,
    missing_kwds={"color": "lightgrey", "label": "Aucune donnée"}
)
ax.set_title("Répartition des Achats par Localisation", fontsize=16)
ax.axis('off')

# Affichage du graphique dans Streamlit
st.pyplot(fig)


# Distribution des Montants des Achats : Boxplot
st.subheader("Distribution des Montants des Achats")

fig, ax = plt.subplots()
ax.boxplot(data['purchase_amount_(usd)'].dropna(), vert=False, patch_artist=True, boxprops=dict(facecolor='skyblue'))
ax.set_title("Distribution des Montants des Achats")
ax.set_xlabel("Montant des Achats (USD)")

# Affiche le graphique
st.pyplot(fig)
