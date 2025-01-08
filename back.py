
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

# Initialisation de l'application FastAPI
app = FastAPI()

# Autorisation des requêtes CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet les requêtes depuis n'importe quelle origine
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Charger les données
data = pd.read_csv("data/shopping_trends.csv")
data.columns = data.columns.str.replace(' ', '_').str.lower()

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

def revenue_by_location(df):
    return df.groupby("location")["purchase_amount_(usd)"].sum().to_dict()

def best_selling_item_by_category(df):
    return df.groupby('category')['item_purchased'].value_counts().groupby('category').idxmax()

# Routes API
@app.get("/kpi/total_revenue")
def get_total_revenue():
    return {"total_revenue": total_revenue(data)}

@app.get("/kpi/average_order_value")
def get_average_order_value():
    return {"average_order_value": average_order_value(data)}

@app.get("/kpi/revenue_by_category")
def get_revenue_by_category():
    return {"revenue_by_category": revenue_by_category(data)}

@app.get("/kpi/most_purchased_item")
def get_most_purchased_item():
    return {"most_purchased_item": most_purchased_item(data)}

@app.get("/kpi/average_review_rating")
def get_average_review_rating():
    return {"average_review_rating": average_review_rating(data)}

@app.get("/kpi/revenue_by_season")
def get_revenue_by_season():
    return {"revenue_by_season": revenue_by_season(data)}

@app.get("/kpi/subscription_percentage")
def get_subscription_percentage():
    return {"subscription_percentage": subscription_percentage(data)}

@app.get("/kpi/promo_code_usage_rate")
def get_promo_code_usage_rate():
    return {"promo_code_usage_rate": promo_code_usage_rate(data)}

@app.get("/kpi/frequent_shopper_rate")
def get_frequent_shopper_rate():
    return {"frequent_shopper_rate": frequent_shopper_rate(data)}

@app.get("/kpi/best_selling_item_by_category")
def get_best_selling_item_by_category():
    return {"best_selling_item_by_category": best_selling_item_by_category(data)}

