from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

# Dictionnaire contenant les noms complets des états américains et leurs abréviations
STATE_ABBREVIATIONS = {
    "alabama": "AL",
    "alaska": "AK",
    "arizona": "AZ",
    "arkansas": "AR",
    "california": "CA",
    "colorado": "CO",
    "connecticut": "CT",
    "delaware": "DE",
    "florida": "FL",
    "georgia": "GA",
    "hawaii": "HI",
    "idaho": "ID",
    "illinois": "IL",
    "indiana": "IN",
    "iowa": "IA",
    "kansas": "KS",
    "kentucky": "KY",
    "louisiana": "LA",
    "maine": "ME",
    "maryland": "MD",
    "massachusetts": "MA",
    "michigan": "MI",
    "minnesota": "MN",
    "mississippi": "MS",
    "missouri": "MO",
    "montana": "MT",
    "nebraska": "NE",
    "nevada": "NV",
    "new hampshire": "NH",
    "new jersey": "NJ",
    "new mexico": "NM",
    "new york": "NY",
    "north carolina": "NC",
    "north dakota": "ND",
    "ohio": "OH",
    "oklahoma": "OK",
    "oregon": "OR",
    "pennsylvania": "PA",
    "rhode island": "RI",
    "south carolina": "SC",
    "south dakota": "SD",
    "tennessee": "TN",
    "texas": "TX",
    "utah": "UT",
    "vermont": "VT",
    "virginia": "VA",
    "washington": "WA",
    "west virginia": "WV",
    "wisconsin": "WI",
    "wyoming": "WY",
}

# Initialisation de l'application FastAPI
app = FastAPI()

# Configuration du middleware CORS pour permettre les requêtes cross-origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise les requêtes de toutes les origines
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les en-têtes HTTP
)

# Chargement des données depuis un fichier CSV
data = pd.read_csv("data/shopping_trends.csv")

# Fonction pour nettoyer les données du DataFrame
def clean_data(df):
    """
    Nettoie et prépare les données pour l'analyse :
    - Supprime les espaces et convertit les colonnes en minuscules.
    - Filtre les valeurs invalides (négatives ou nulles).
    - Ajoute une colonne pour les groupes d'âge.
    """
    # Nettoyage des colonnes (enlève les espaces et les met en minuscules)
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()

    # Supprime les lignes avec des valeurs manquantes
    df = df.dropna()

    # Colonnes textuelles à nettoyer
    text_columns = [
        "gender",
        "category",
        "location",
        "season",
        "payment_method",
        "shipping_type",
        "discount_applied",
        "promo_code_used",
        "frequency_of_purchases",
        "subscription_status",
    ]
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].str.strip().str.lower()

    # Conversion des colonnes numériques en types corrects
    if "purchase_amount_(usd)" in df.columns:
        df["purchase_amount_(usd)"] = pd.to_numeric(
            df["purchase_amount_(usd)"], errors="coerce"
        )

    if "review_rating" in df.columns:
        df["review_rating"] = pd.to_numeric(df["review_rating"], errors="coerce")

    if "age" in df.columns:
        # Filtre les âges invalides (par exemple, négatifs ou > 100)
        df = df[(df["age"] > 0) & (df["age"] < 100)]

    if "purchase_amount_(usd)" in df.columns:
        # Supprime les montants d'achat <= 0
        df = df[df["purchase_amount_(usd)"] > 0]

    # Ajout d'une colonne pour les groupes d'âge
    bins = [0, 18, 30, 40, 50, 60, 70, 80, 90, 100]
    labels = ['0-18', '18-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)
    df['age_group'] = df['age_group'].astype(str)

    return df

# Nettoyage des données au moment du chargement
data = clean_data(data)

# Fonction pour transformer les noms de régions en abréviations
def transform_region_data(data):
    transformed_data = {}
    for region, value in data.items():
        abbreviation = STATE_ABBREVIATIONS.get(region.lower())
        if abbreviation:
            transformed_data[abbreviation] = value
    return transformed_data

# Fonctions KPI

# Calcule le revenu total des données.
def total_revenue(df):
    return df["purchase_amount_(usd)"].sum()

# Calcule la valeur moyenne des commandes.
def average_order_value(df):
    return df["purchase_amount_(usd)"].mean()

# Calcule le revenu par catégorie.
def revenue_by_category(df):
    return df.groupby("category")["purchase_amount_(usd)"].sum().to_dict()

# Retourne l'article le plus acheté.
def most_purchased_item(df):
    return df["item_purchased"].value_counts().idxmax()

# Calcule la moyenne des notes d'avis.
def average_review_rating(df):
    return df["review_rating"].mean()

# Calcule le revenu par saison.
def revenue_by_season(df):
    return df.groupby("season")["purchase_amount_(usd)"].sum().to_dict()

# Calcule le pourcentage de clients abonnés.
def subscription_percentage(df):
    subscribers = df[df["subscription_status"] == "yes"]
    return (len(subscribers) / len(df)) * 100

# Calcule le taux d'utilisation des codes promo.
def promo_code_usage_rate(df):
    promo_used = df[df["promo_code_used"] == "yes"]
    return (len(promo_used) / len(df)) * 100

# Calcule le pourcentage d'acheteurs fréquents.
def frequent_shopper_rate(df):
    frequent_shoppers = df[df["frequency_of_purchases"].isin(["weekly", "fortnightly"])]
    return (len(frequent_shoppers) / len(df)) * 100

# Calcule le revenu par localisation.
def revenue_by_location(df):
    return df.groupby("location")["purchase_amount_(usd)"].sum().to_dict()

# Trouve l'article le plus vendu par catégorie.
def best_selling_item_by_category(df):
    return df.groupby('category')['item_purchased'].value_counts().groupby('category').idxmax()

# Calcule la proportion de clients abonnés qui sont des acheteurs fréquents.
def subscriber_frequent_relation(df):
    subscribers = df[df["subscription_status"] == "yes"]
    frequent_subscribers = subscribers[
        subscribers["frequency_of_purchases"].isin(["weekly", "fortnightly"])
    ]

    proportion_frequent_among_subscribers = (len(frequent_subscribers) / len(subscribers)) * 100 if len(subscribers) > 0 else 0

    return {"frequent_shoppers_among_subscribers": proportion_frequent_among_subscribers,}

# Calcule l'article le plus vendu.
def customer_age_rate(df):
    return df['age_group'].value_counts().to_dict()


# Routes API pour les KPI
@app.get("/kpi/total_revenue")
def get_total_revenue():
    """
    Retourne la somme de purchase_amount_(usd) pour avoir la valeur totale des revenus.
    """
    total = total_revenue(data)
    return {"total": str(total)}

@app.get("/kpi/revenue_by_location")
def get_revenue_by_location():
    """
    Retourne le revenu par localisation avec transformation des régions.
    """
    revenue_data = revenue_by_location(data)
    transformed_revenue_data = transform_region_data(revenue_data)
    return {"revenue_by_location": transformed_revenue_data}

@app.get("/kpi/customer_age_rate")
def get_customer_age_rate():
    """
    Retourne la répartition des clients par groupes d'âge.
    """
    return {"customer_age_rate": customer_age_rate(data)}

@app.get("/kpi/average_order_value")
def get_average_order_value():
    """
    Retourne la valeur moyenne de df["purchase_amount_(usd)"].
    """
    return {"average_order_value": average_order_value(data)}

@app.get("/kpi/revenue_by_category")
def get_revenue_by_category():
    """
    Retourne le revenu par catégorie. La somme de ["purchase_amount_(usd)"] trié par catégories et converti en dictionnaire
    """
    return {"revenue_by_category": revenue_by_category(data)}

@app.get("/kpi/most_purchased_item")
def get_most_purchased_item():
    """
    Retourne l'article le plus acheté. ['item_purchased'] avec le plus grand nombre d'occurrences.
    """
    return {"most_purchased_item": most_purchased_item(data)}

@app.get("/kpi/average_review_rating")
def get_average_review_rating():
    """
    Retourne la moyenne des notes d'avis ['review_rating'].
    """
    return {"average_review_rating": average_review_rating(data)}

@app.get("/kpi/revenue_by_season")
def get_revenue_by_season():
    """
    Calcule la somme des montants d'achat (en USD) pour chaque saison, puis convertit le résultat en un dictionnaire.
    """
    return {"revenue_by_season": revenue_by_season(data)}

@app.get("/kpi/subscription_percentage")
def get_subscription_percentage():
    """
    Retourne le pourcentage d'abonnés. Somme des subscription_status = "yes" divisé par le nombre total de clients.
    """
    return {"subscription_percentage": subscription_percentage(data)}

@app.get("/kpi/promo_code_usage_rate")
def get_promo_code_usage_rate():
    """
    ["promo_code_used"] == "yes" / nombre total d'acheteurs.
    """
    return {"promo_code_usage_rate": promo_code_usage_rate(data)}

@app.get("/kpi/frequent_shopper_rate")
def get_frequent_shopper_rate():
    """
    Nombre d'acheteur qui sont ["weekly"] | ["fortnightly"] / nombre total d'acheteurs.
    """
    return {"frequent_shopper_rate": frequent_shopper_rate(data)}

@app.get("/kpi/best_selling_item_by_category")
def get_best_selling_item_by_category():
    """
    Retourne l'article le plus vendu par catégorie.
    """
    return {"best_selling_item_by_category": best_selling_item_by_category(data)}

@app.get("/kpi/subscriber_frequent_relation")
def get_subscriber_frequent_relation():
    """
    Retourne la proportion d'abonnés qui sont des acheteurs fréquents.
    """
    return {"subscriber_frequent_relation": subscriber_frequent_relation(data)}
