from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pymongo import MongoClient
import happybase
from collections import Counter
import json
import os

print("✅ Script started...")

# -------------------------------
# STEP 1: Load data from MongoDB
# -------------------------------
print("📦 Connecting to MongoDB...")
client = MongoClient("mongodb://localhost:27017")
db = client['ecommerce_db']

users = pd.DataFrame(list(db.users.find({}, {"_id": 0})))
products_info = pd.DataFrame(list(db.products.find({}, {"_id": 0, "product_id": 1, "name": 1, "base_price": 1, "category": 1})))
transactions = pd.DataFrame(list(db.transactions.find({}, {"_id": 0, "user_id": 1, "timestamp": 1, "items": 1, "total": 1})))
categories = pd.DataFrame(list(db.categories.find({}, {"_id": 0})))  # ✅ NEW: Load categories

# -------------------------------
# DATASET SUMMARY METRICS
# -------------------------------
num_users = len(users)
num_products = len(products_info)
num_categories = len(categories)
num_transactions = len(transactions)

# ✅ Print MongoDB load message with commas
print(f"✅ Loaded {num_users:,} users, {num_products:,} products, {num_categories:,} categories, {num_transactions:,} transactions from MongoDB")

# -------------------------------
# STEP 2: Load data from HBase
# -------------------------------
print("📡 Connecting to HBase...")
connection = happybase.Connection('localhost', timeout=300000)
table = connection.table('user_sessions')

print("🔁 Scanning HBase sessions...")
session_list = []
for key, data in table.scan():
    try:
        user_key = key.decode()
        user_id = "_".join(user_key.split("_")[:2])
        viewed = eval(data.get(b'info:viewed_products', b'[]').decode())
        cart = eval(data.get(b'info:cart_contents', b'{}').decode()).keys()
        session_list.append({"user_id": user_id, "viewed": list(viewed), "carted": list(cart)})
    except:
        continue

session_df = pd.DataFrame(session_list)
print(f"✅ Loaded {len(session_list):,} sessions from HBase")  # ✅ formatted with comma

num_sessions = len(session_df)

summary_data = pd.DataFrame({
    "Metric": ["Users", "Products", "Categories", "Transactions", "Sessions"],
    "Count": [num_users, num_products, num_categories, num_transactions, num_sessions]
})

# -------------------------------
# MAIN PLOTS
# -------------------------------
print("📊 Building visualizations...")
# Business Question 2: How has our total sales performance evolved over the past three months?
# Answered in: main.py → Plot 1 (line graph)
transactions['timestamp'] = pd.to_datetime(transactions['timestamp'])
transactions['date'] = transactions['timestamp'].dt.date
sales_by_date = transactions.groupby('date')['total'].sum().reset_index()
fig1 = px.line(sales_by_date, x='date', y='total', title="PLOT 1: Sales Performance Over Time")
fig1.update_layout(xaxis_tickangle=-45, bargap=0.2, xaxis=dict(categoryorder='total descending'), height=600, autosize=True)

users['registration_date'] = pd.to_datetime(users['registration_date'])
users['reg_year'] = users['registration_date'].dt.year
merged = pd.merge(transactions, users, on='user_id', how='inner')
avg_spend = merged.groupby('reg_year')['total'].mean().reset_index()
fig2 = px.bar(avg_spend, x='reg_year', y='total', title="PLOT 2: Avg Spending by Registration Year")
fig2.update_layout(xaxis_tickangle=-45, bargap=0.2, xaxis=dict(categoryorder='total descending'), height=600, autosize=True)

# Business Question three:
## Which products are the most purchased in terms of quantity?
product_counter = Counter()
for txn in transactions["items"]:
    for item in txn:
        pid = item["product_id"]
        qty = item["quantity"]
        product_counter[pid] += qty

product_df = pd.DataFrame(product_counter.items(), columns=["product_id", "quantity"])
product_df = product_df.sort_values("quantity", ascending=False).head(10)
product_df = product_df.merge(products_info, on="product_id", how="left")
product_df["total_amount"] = product_df["quantity"] * product_df["base_price"]
product_df["label"] = product_df.apply(lambda row: f"{row['name']}<br>({row['product_id']})<br>Price: ${row['base_price']:.2f}<br>Total: ${row['total_amount']:.2f}", axis=1)
fig3 = px.bar(product_df, x="label", y="quantity", title="PLOT 3: Top 10 Products Purchased")
fig3.update_layout(xaxis_tickangle=-45, bargap=0.2, xaxis=dict(categoryorder='total descending'), height=800, autosize=True)

# Business Question 1: What is the user conversion funnel from browsing to purchase?
# Answered in: main.py → Plot 4 using HBase + MongoDB
funnel_counts = {"Viewed": 0, "Added to Cart": 0, "Converted": 0}
for key, data in table.scan():
    try:
        raw = {k.decode().split(":")[1]: v.decode() for k, v in data.items()}
        viewed = json.loads(raw.get("viewed_products", "[]"))
        carted = json.loads(raw.get("cart_contents", "{}"))
        converted = raw.get("conversion", "")
        if viewed:
            funnel_counts["Viewed"] += 1
        if carted:
            funnel_counts["Added to Cart"] += 1
        if converted == "converted":
            funnel_counts["Converted"] += 1
    except:
        continue

fig4 = go.Figure(go.Funnel(
    y=list(funnel_counts.keys()),
    x=list(funnel_counts.values()),
    textinfo="value+percent initial"
))
fig4.update_layout(title="PLOT 4: Conversion Funnel", height=800)

# -------------------------------
# Load CSV Results from External Scripts
# -------------------------------
print("📂 Reading cohort_output.csv, spark_sql_output.csv, output_revenue_by_product_and_category.csv, output_top_selling_products_named.csv, hbase_user_sessions.csv and hbase_user_summary.csv")
cohort_output = pd.read_csv("cohort_output.csv") if os.path.exists("cohort_output.csv") else pd.DataFrame()
sql_output = pd.read_csv("spark_sql_output.csv") if os.path.exists("spark_sql_output.csv") else pd.DataFrame()
revenue_by_product_and_category_output = pd.read_csv("output_revenue_by_product_and_category.csv") if os.path.exists("output_revenue_by_product_and_category.csv") else pd.DataFrame()
top_selling_products_output = pd.read_csv("output_top_selling_products_named.csv") if os.path.exists("output_top_selling_products_named.csv") else pd.DataFrame()
hbase_user_sessions_output = pd.read_csv("hbase_user_sessions.csv") if os.path.exists("hbase_user_sessions.csv") else pd.DataFrame()
hbase_user_summary_output = pd.read_csv("hbase_user_summary.csv") if os.path.exists("hbase_user_summary.csv") else pd.DataFrame()
print("🚀 Ready to launch Dash app")

# -------------------------------
# DASH APP
# -------------------------------
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "E-commerce Dashboard"

app.layout = dbc.Container([
    html.H1("📊 E-commerce Analytics Dashboard", className="text-center my-4"),
    dcc.Tabs([
        dcc.Tab(label="🔢 Dataset Summary", children=[
            html.H2("Dataset Overview Metrics", className="my-3"),
            dbc.Table.from_dataframe(
                summary_data.assign(Count=summary_data["Count"].apply(lambda x: f"{x:,}")),
                striped=True, bordered=True, hover=True
            )
        ]),
        dcc.Tab(label="📈 Main Dashboard", children=[
            html.H2("PLOT 1: Sales Performance Over Time"), dcc.Graph(figure=fig1),
            html.H2("PLOT 2: Customer Segmentation by Year"), dcc.Graph(figure=fig2),
            html.H2("PLOT 3: Product Performance (Top 10)"), dcc.Graph(figure=fig3),
            html.H2("PLOT 4: Conversion Funnel"), dcc.Graph(figure=fig4),
        ]),
        dcc.Tab(label="🟦 Cohort Analysis", children=[
            html.H2("User Cohort Table: cohort_month= Users who did registration and tx_month= Users who made transactions"),
            dbc.Table.from_dataframe(cohort_output, striped=True, bordered=True, hover=True) if not cohort_output.empty else html.P("No cohort_output.csv available")
        ]),
        dcc.Tab(label="🟩 Spark SQL Analysis", children=[
            html.H2("Category-Level Sales Summary: Total Revenue by Product Category"),
            dbc.Table.from_dataframe(sql_output, striped=True, bordered=True, hover=True) if not sql_output.empty else html.P("No spark_sql_output.csv available")
        ]),
        dcc.Tab(label="🟥 Product popularity analysis", children=[
            html.H2("Top-Selling Products"),
            dbc.Table.from_dataframe(top_selling_products_output, striped=True, bordered=True, hover=True) if not sql_output.empty else html.P("No output_top_selling_products_named.csv available")
        ]),
        dcc.Tab(label="⬛ Revenue analytics", children=[
            html.H2("Revenue by Product with Category"),
            dbc.Table.from_dataframe(revenue_by_product_and_category_output, striped=True, bordered=True, hover=True) if not sql_output.empty else html.P("No output_revenue_by_product_and_category.csv available")
        ]),
        dcc.Tab(label="🟫 Full sessions for this user (user_id = user_000042)", children=[
            html.H2("Exported all session data"),
            dbc.Table.from_dataframe(hbase_user_sessions_output, striped=True, bordered=True, hover=True) if not sql_output.empty else html.P("No hbase_user_sessions.csv available")
        ]),
        dcc.Tab(label="🟨 Summary (Total Sessions + Duration)", children=[
            html.H2("Exported session summary"),
            dbc.Table.from_dataframe(hbase_user_summary_output, striped=True, bordered=True, hover=True) if not sql_output.empty else html.P("No hbase_user_summary.csv available")
        ]),
    ])
], fluid=True)

if __name__ == '__main__':
    print("🌐 Opening Dash app on http://127.0.0.1:8050")
    app.run(debug=True, host="127.0.0.1", port=8050)
