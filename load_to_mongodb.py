from pymongo import MongoClient
import json

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce_db"]

# Load users
with open("users.json") as f:
    users = json.load(f)
db.users.insert_many(users)

# Load products
with open("products.json") as f:
    products = json.load(f)
db.products.insert_many(products)

# Load categories
with open("categories.json") as f:
    categories = json.load(f)
db.categories.insert_many(categories)

# Load transactions
with open("transactions.json") as f:
    transactions = json.load(f)
db.transactions.insert_many(transactions)

print("✅ All data loaded into MongoDB successfully.")
