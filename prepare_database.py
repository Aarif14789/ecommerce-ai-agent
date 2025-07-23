import pandas as pd
import sqlite3

# Load CSVs or raw data into pandas DataFrames
ad_sales = pd.read_csv("data/ad_sales.csv")
total_sales = pd.read_csv("data/total_sales.csv")
eligibility = pd.read_csv("data/eligibility.csv")

# Connect to SQLite DB
conn = sqlite3.connect("ecommerce.db")

# Write data to SQLite tables
ad_sales.to_sql("ad_sales", conn, if_exists="replace", index=False)
total_sales.to_sql("total_sales", conn, if_exists="replace", index=False)
eligibility.to_sql("eligibility", conn, if_exists="replace", index=False)

conn.close()
print("✅ Database prepared successfully.")
