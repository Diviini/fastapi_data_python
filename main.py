import pandas as pd
from fastapi import FastAPI

def clean_data(df):
    """
    Clean the dataset by addressing common data issues.
    """
    # Clean column names
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()

    # Handle missing values
    df = df.dropna()  # Drop rows with missing values

    # Standardize text columns
    text_columns = ['gender', 'category', 'location', 'season', 'payment_method',
                    'shipping_type', 'discount_applied', 'promo_code_used', 'frequency_of_purchases', 'subscription_status']
    for col in text_columns:
        df[col] = df[col].str.strip().str.lower()

    # Convert numerical columns to appropriate types
    df['purchase_amount_(usd)'] = pd.to_numeric(df['purchase_amount_(usd)'], errors='coerce')
    df['review_rating'] = pd.to_numeric(df['review_rating'], errors='coerce')

    # Handle outliers for age and purchase amount
    df = df[(df['age'] > 0) & (df['age'] < 100)]
    df = df[df['purchase_amount_(usd)'] > 0]

    return df

# KPI Functions
def total_revenue(df):
    """Calculate total revenue."""
    return df['purchase_amount_(usd)'].sum()


def average_order_value(df):
    """Calculate average order value."""
    return df['purchase_amount_(usd)'].mean()

def revenue_by_category(df):
    """Calculate revenue by category."""
    return df.groupby('category')['purchase_amount_(usd)'].sum().to_dict()

def most_purchased_item(df):
    """Find the most purchased item."""
    return df['item_purchased'].value_counts().idxmax()

def average_review_rating(df):
    """Calculate average review rating."""
    return df['review_rating'].mean()

def revenue_by_season(df):
    """Calculate revenue by season."""
    return df.groupby('season')['purchase_amount_(usd)'].sum().to_dict()

def subscription_percentage(df):
    """Calculate the percentage of subscribed customers."""
    subscribed = df[df['subscription_status'] == 'yes']
    return (len(subscribed) / len(df)) * 100

def promo_code_usage_rate(df):
    """Calculate the usage rate of promo codes."""
    promo_used = df[df['promo_code_used'] == 'yes']
    return (len(promo_used) / len(df)) * 100

def frequent_shopper_rate(df):
    """Calculate the rate of frequent shoppers."""
    frequent = df[df['frequency_of_purchases'].isin(['weekly', 'fortnightly'])]
    return (len(frequent) / len(df)) * 100

def revenue_by_location(df):
    """Calculate revenue by location."""
    return df.groupby('location')['purchase_amount_(usd)'].sum().to_dict()

# Load and clean data
pd.set_option("display.max_columns", None)

data = pd.read_csv('data/shopping_trends.csv')
data = clean_data(data)

app = FastAPI()

# FastAPI Routes
@app.get("/kpi/")
def get_total_revenue():
    return {"total_revenue": 1}

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

@app.get("/kpi/revenue_by_location")
def get_revenue_by_location():
    return {"revenue_by_location": revenue_by_location(data)}

import matplotlib.pyplot as plt

# Revenu par catégorie
def plot_revenue_by_category(df):
    revenue = revenue_by_category(df)
    categories = list(revenue.keys())
    values = list(revenue.values())

    plt.figure(figsize=(10, 6))
    plt.bar(categories, values, color='skyblue')
    plt.title('Revenue by Category')
    plt.xlabel('Category')
    plt.ylabel('Revenue (USD)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('revenue_by_category.png')  # Save the plot as an image
    plt.show()

# Taux de souscription
def plot_subscription_percentage(df):
    percentage = subscription_percentage(df)
    labels = ['Subscribed', 'Not Subscribed']
    sizes = [percentage, 100 - percentage]
    colors = ['lightgreen', 'lightcoral']

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
    plt.title('Subscription Percentage')
    plt.savefig('subscription_percentage.png')  # Save the plot as an image
    plt.show()

# Taux d'utilisation des codes promo
def plot_promo_code_usage_rate(df):
    usage_rate = promo_code_usage_rate(df)
    labels = ['Promo Code Used', 'No Promo Code Used']
    sizes = [usage_rate, 100 - usage_rate]
    colors = ['gold', 'lightgrey']

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
    plt.title('Promo Code Usage Rate')
    plt.savefig('promo_code_usage_rate.png')  # Save the plot as an image
    plt.show()

# Appel des fonctions pour tester
plot_revenue_by_category(data)
plot_subscription_percentage(data)
plot_promo_code_usage_rate(data)