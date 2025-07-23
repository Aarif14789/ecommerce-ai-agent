from llm_sql import question_to_sql_groq

question = "What is the total sales on 1st June 2025?"
sql = question_to_sql_groq(question)
print("✅ Clean SQL:\n", sql)
