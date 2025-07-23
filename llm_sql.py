import re
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

system_prompt = """
You are an assistant that translates natural language questions into SQL queries.
The database has 3 tables: ad_sales, total_sales, and eligibility.

Table: ad_sales
Columns: date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold

Table: total_sales
Columns: date, item_id, total_sales, total_units_ordered

Table: eligibility
Columns: eligibility_datetime_utc, item_id, eligibility, message

Some derived metrics:
- RoAS (Return on Ad Spend) = SUM(ad_sales) / SUM(ad_spend)
- CPC (Cost Per Click) = ad_spend / clicks

Use the date '2025-06-01' unless the user specifies another date.

⚠️ IMPORTANT: Return only ONE valid SQLite SQL query.
Do NOT return multiple SQL statements together.
Do NOT include markdown or explanation.
""".strip()


def question_to_sql_groq(question: str) -> str:
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0.2,
    )

    raw_output = response.choices[0].message.content

    # Clean up the response to extract SQL
    sql = re.sub(r"```sql|```", "", raw_output).strip()
    return sql
