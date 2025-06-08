# ecommerce-bigdata-analytics
# 🛒 Distributed Multi-Model Analytics for E-commerce Data

This project implements a full-stack Big Data Analytics system combining MongoDB, HBase, Apache Spark, and Python to analyze large-scale e-commerce data. Built as part of a Master's in Big Data Analytics final project.

---

## 📦 Technologies Used

- **MongoDB**: For storing structured documents (users, products, transactions)
- **HBase**: For session logs in wide-column format
- **Apache Spark (PySpark)**: For distributed processing and analytics
- **Python + Pandas**: For ETL and transformations
- **Dash + Plotly**: For interactive web dashboard
- **HappyBase**: Python interface for HBase

---

## 📁 Project Directory Tree
├── env/                              # Python virtual environment folder
├── jars/                             # Spark/Hadoop jars (optional)
├── cohort_analysis.py                # PySpark cohort analysis script
├── cohort_output.csv                 # Output CSV from cohort analysis
├── dataset_generator.py              # Synthetic dataset generator script
├── Final exam Big Data Analytics Report.pdf  # Final written report
├── hbase_user_session_export.py      # HBase session exporter script
├── hbase_user_sessions.csv           # Exported session-level data
├── hbase_user_summary.csv            # HBase summary data
├── insert_sessions_hbase.py          # Script to insert sessions into HBase
├── load_to_mongodb.py                # Script to load data into MongoDB
├── main.py                           # Dash dashboard script
├── mongo_aggregations.py             # MongoDB aggregation analytics
├── output_revenue_by_product_and_category.csv  # Revenue analytics output
├── output_top_selling_products_named.csv       # Top-selling product output
├── README.md                         # Main documentation
├── spark_sql_analysis.py             # Spark SQL revenue analysis
├── spark_sql_output.csv              # Output from Spark SQL queries
├── start_all_hbase.bat               # Batch file to start Hadoop and HBase
├── stop_all_hbase.bat                # Batch file to stop Hadoop and HBase

---

**🛠️ How to Run the System**

**⚙️ Start Hadoop + HBase Services (Required)**

HBase runs on top of Hadoop, so make sure Hadoop is started first.

**Use these batch files to simplify startup on Windows:**

➤ start_all_hbase.bat    # Starts Hadoop daemons + HBase master + RegionServer

**To stop everything:**
➤ stop_all_hbase.bat     # Stops HBase and Hadoop services

**1.Generate Synthetic Dataset**
➤ python dataset_generator.py

**2.Insert into MongoDB**
➤ python load_to_mongodb.py

**3.Insert Sessions into HBase**
➤ python insert_sessions_hbase.py

**4.Run Analytics**
# MongoDB Aggregations
➤ python mongo_aggregations.py

# Cohort Analysis
➤ python cohort_analysis.py

# Revenue by Category (Spark SQL)
➤ python spark_sql_analysis.py

**5.Launch Dashboard**
➤ python main.py
Then open in your browser: http://127.0.0.1:8050

**📊 Dashboard Features**

PLOT 1: 📈 Sales Performance Over Time➤ Total daily sales from March to May 2025

PLOT 2: 👥 Customer Segmentation by Registration Year➤ Average spending behavior by registration year

PLOT 3: 🏆 Top 10 Products Purchased➤ Based on quantity sold and revenue

PLOT 4: 🔁 Conversion Funnel➤ User progression: Viewed → Added to Cart → Purchased

**❓ Business Questions Answered:**

➤ What is the user conversion funnel from browsing to purchase?

➤ How has our total sales performance evolved over the past three months?

➤ Which products are the most purchased in terms of quantity?

**📄 Dataset Usage Note**

**This project is designed to demonstrate distributed data modeling:**

**The following 4 files are stored in MongoDB:**

➤ users.json, categories.json, products.json, transactions.json

➤ The session logs (sessions_*.json) containing over 2,000,000 records are loaded into HBase.

**⚠️ Due to GitHub's 100MB file limit, the full dataset (especially sessions files)**

**📘 Report Summary**

**The full project report (Final_Big_Data_Analytics_Report.docx) contains:**

➤ System architecture

➤ MongoDB & HBase schema design

➤ Spark data processing pipelines

➤ Cohort & funnel analysis

➤ Key business insights

➤ Recommendations for improvement

**👨‍🎓 Student Info**
Name: NIYONSENGA Jean Paul

Student ID: 100888

Program: Master's in Big Data Analytics

Course: Big Data Analytics

Lecturer: Temitope Oguntade

Due Date: June 8th, 2025


