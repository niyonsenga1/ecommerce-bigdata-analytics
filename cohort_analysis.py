# from pyspark.sql import SparkSession
# from pyspark.sql.functions import col, to_date, trunc, countDistinct, month, year, expr

# # Step 1: Start Spark Session
# spark = SparkSession.builder.appName("CohortAnalysis").getOrCreate()

# # Step 2: Load Users and Transactions
# users_df = spark.read.option("multiline", True).json("users.json")
# tx_df = spark.read.option("multiline", True).json("transactions.json")

# # Step 3: Prepare user cohort month
# users_df = users_df.withColumn("cohort_month", trunc(to_date("registration_date"), "MM"))

# # Step 4: Prepare transaction month
# tx_df = tx_df.withColumn("tx_month", trunc(to_date("timestamp"), "MM"))

# # Step 5: Join users with their transactions
# cohort_df = tx_df.join(users_df, on="user_id")

# # Step 6: Group by cohort and transaction month
# result = cohort_df.groupBy("cohort_month", "tx_month").agg(
#     countDistinct("user_id").alias("active_users")
# ).orderBy("cohort_month", "tx_month")

# # Step 7: Show results
# result.show(20, False)
# cohort_analysis.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, trunc, countDistinct

# Step 1: Start Spark Session
spark = SparkSession.builder.appName("CohortAnalysis").getOrCreate()

# Step 2: Load Users and Transactions
users_df = spark.read.option("multiline", True).json("users.json")
tx_df = spark.read.option("multiline", True).json("transactions.json")

# Step 3: Prepare user cohort month
users_df = users_df.withColumn("cohort_month", trunc(to_date("registration_date"), "MM"))

# Step 4: Prepare transaction month
tx_df = tx_df.withColumn("tx_month", trunc(to_date("timestamp"), "MM"))

# Step 5: Join users with their transactions
cohort_df = tx_df.join(users_df, on="user_id")

# Step 6: Group by cohort and transaction month
result = cohort_df.groupBy("cohort_month", "tx_month").agg(
    countDistinct("user_id").alias("active_users")
).orderBy("cohort_month", "tx_month")

# Step 7: Save result as CSV for dashboard
result.coalesce(1).toPandas().to_csv("cohort_output.csv", index=False)
print("✅ Cohort output saved to cohort_output.csv")
