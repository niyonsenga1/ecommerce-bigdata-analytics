import pymongo
import pandas as pd

# 🔌 Step 1: Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
db = client["ecommerce_db"]  # ← HINDURA niba database yawe ifite irindi zina

# Business Question three:
## Which products are the most purchased in terms of quantity?
# ------------------------------------------
# 📊 PIPELINE 1: Top-Selling Products with Product Name
print("📊 Running: Top-Selling Products with Product Names...")
pipeline_popular_products_named = [
    {"$unwind": "$items"},
    {"$group": {
        "_id": "$items.product_id",
        "total_quantity_sold": {"$sum": "$items.quantity"}
    }},
    {"$sort": {"total_quantity_sold": -1}},
    {"$limit": 10},
    {"$lookup": {
        "from": "products",
        "localField": "_id",
        "foreignField": "product_id",
        "as": "product_info"
    }},
    {"$unwind": "$product_info"},
    {"$project": {
        "_id": 0,
        "product_id": "$_id",
        "product_name": "$product_info.name",
        "total_quantity_sold": 1
    }}
]

try:
    result1 = list(db.transactions.aggregate(pipeline_popular_products_named))
    df_popular_named = pd.DataFrame(result1)
    df_popular_named.to_csv("output_top_selling_products_named.csv", index=False)
    print("✅ Saved: output_top_selling_products_named.csv")
except Exception as e:
    print(f"⛔ Error in Pipeline 1: {e}")

# ------------------------------------------
# 💰 PIPELINE 2: Revenue by Product with Category & Product Names
print("💰 Running: Revenue by Product with Category & Product Names...")
pipeline_revenue_with_product_and_category_name = [
    {"$unwind": "$items"},
    {"$limit": 1000},  # TEMP: increase or remove for full dataset

    {"$lookup": {
        "from": "products",
        "localField": "items.product_id",
        "foreignField": "product_id",
        "as": "product_info"
    }},
    {"$unwind": "$product_info"},

    {"$lookup": {
        "from": "categories",
        "localField": "product_info.category_id",
        "foreignField": "category_id",
        "as": "category_info"
    }},
    {"$unwind": "$category_info"},

    {"$group": {
        "_id": "$items.product_id",
        "product_name": {"$first": "$product_info.name"},
        "category_id": {"$first": "$product_info.category_id"},
        "category_name": {"$first": "$category_info.name"},
        "total_revenue": {"$sum": "$items.subtotal"}
    }},
    {"$sort": {"total_revenue": -1}}
]

try:
    result2 = list(db.transactions.aggregate(pipeline_revenue_with_product_and_category_name))
    if result2:
        df_prod_cat_revenue = pd.DataFrame(result2)
        df_prod_cat_revenue.rename(columns={"_id": "product_id"}, inplace=True)
        df_prod_cat_revenue.to_csv("output_revenue_by_product_and_category.csv", index=False)
        print("✅ Saved: output_revenue_by_product_and_category.csv")
    else:
        print("⚠️ No matching product or category data found.")
except Exception as e:
    print(f"⛔ Error in Pipeline 2: {e}")

print("\n🎉 DONE: Aggregation pipelines executed successfully.")
