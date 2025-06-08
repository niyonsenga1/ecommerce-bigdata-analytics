# from pyspark.sql import SparkSession
# from pyspark.sql.functions import explode, col, expr

# # STEP 1: Start Spark Session
# spark = SparkSession.builder.appName("SparkSQLAnalytics").getOrCreate()

# # STEP 2: Load JSON files
# products_df = spark.read.option("multiline", True).json("products.json")
# tx_df = spark.read.option("multiline", True).json("transactions.json")

# # STEP 3: Prepare exploded transactions
# tx_items = tx_df.withColumn("item", explode("items")) \
#     .select(
#         col("user_id"),
#         col("timestamp"),
#         col("item.product_id").alias("product_id"),
#         col("item.subtotal").alias("subtotal")
#     )

# # STEP 4: Register DataFrames as temporary SQL tables
# tx_items.createOrReplaceTempView("transactions")
# products_df.createOrReplaceTempView("products")

# # STEP 5: Run Spark SQL query
# query = """
# SELECT 
#     p.category_id,
#     COUNT(t.product_id) AS total_sales,
#     ROUND(SUM(t.subtotal), 2) AS total_revenue
# FROM transactions t
# JOIN products p ON t.product_id = p.product_id
# GROUP BY p.category_id
# ORDER BY total_revenue DESC
# """

# result_df = spark.sql(query)

# # STEP 6: Show the result
# result_df.show(10, False)
# spark_sql_analysis.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col

# STEP 1: Start Spark Session
spark = SparkSession.builder.appName("SparkSQLAnalytics").getOrCreate()

# STEP 2: Load JSON files
products_df = spark.read.option("multiline", True).json("products.json")
tx_df = spark.read.option("multiline", True).json("transactions.json")

# STEP 3: Prepare exploded transactions
tx_items = tx_df.withColumn("item", explode("items")) \
    .select(
        col("user_id"),
        col("timestamp"),
        col("item.product_id").alias("product_id"),
        col("item.subtotal").alias("subtotal")
    )

# STEP 4: Register DataFrames as temporary SQL tables
tx_items.createOrReplaceTempView("transactions")
products_df.createOrReplaceTempView("products")

#Category-Level Sales Summary: Total Revenue by Product Category
# STEP 5: Run Spark SQL query
query = """
SELECT 
    p.category_id,
    COUNT(t.product_id) AS total_sales,
    ROUND(SUM(t.subtotal), 2) AS total_revenue
FROM transactions t
JOIN products p ON t.product_id = p.product_id
GROUP BY p.category_id
ORDER BY total_revenue DESC
"""

result_df = spark.sql(query)

# STEP 6: Save result to CSV for dashboard
result_df.coalesce(1).toPandas().to_csv("spark_sql_output.csv", index=False)
print("✅ Spark SQL output saved to spark_sql_output.csv")

