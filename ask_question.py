import sqlite3
import pandas as pd
from llm_sql import question_to_sql_groq

# Step 1: Ask your question
question = "What is the total sales on 1st June 2025?"

# Step 2: Convert to SQL using Groq
sql = question_to_sql_groq(question)
print("🧠 Generated SQL:\n", sql)

# Step 3: Connect to SQLite database
conn = sqlite3.connect("db/ecommerce.db")

try:
    # Step 4: Run the SQL
    df = pd.read_sql_query(sql, conn)
    print("\n📊 Query Result:")
    print(df)
except Exception as e:
    print("\n❌ Error running query:")
    print(str(e))
finally:
    conn.close()
