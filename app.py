import os
import pymysql
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()
api_key = os.getenv("gemini_api_key")
genai.configure(api_key=api_key)

# Model
model = genai.GenerativeModel("gemini-2.5-flash")

# Streamlit UI
st.set_page_config(page_title="AI SQL Chatbot", layout="centered")
st.title("💬 AI SQL Chatbot (MySQL + Gemini)")


# MySQL connection
conn = pymysql.connect(
    host="localhost",
    user="root",
    password=os.getenv("db_password"),
    database="pallavidb",
    cursorclass=pymysql.cursors.DictCursor
)

def get_sql_from_llm(question,schema_info):
    prompt = f"""
    You are a SQL assistant. Convert the question into a valid MySQL query.

    Database schema:{schema_info}
    
    Question: {question}
    Answer: Return only SQL query,Nothing else.Do not include ```sql fences or explanations.

    """
    #model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text

def run_query(sql):
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()
    
def natural_answer(question, rows):
    """Use Gemini to convert SQL result into a natural language answer"""
    prompt = f"""
    The user asked: {question}
    The SQL result is: {rows}

    Write a short, clear natural language answer to the question using the result.
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# --- Streamlit app logic ---
st.subheader("Ask a question about your database 👇")


# # ---- Main loop ----
if __name__ == "__main__":
    # Get schema once
    schema = {}
    with conn.cursor() as cur:
        cur.execute("SHOW TABLES;")
        tables = [list(row.values())[0] for row in cur.fetchall()]
        for t in tables:
            cur.execute(f"SHOW COLUMNS FROM {t};")
            cols = [row['Field'] for row in cur.fetchall()]
            schema[t] = cols

    schema_text = "\n".join([f"{t}({', '.join(cols)})" for t, cols in schema.items()])


q= st.text_input("Your question:")

if st.button("Get Answer") and q:
    with st.spinner("Generating SQL & fetching results..."):
        sql = get_sql_from_llm(q, schema_text)
        st.code(sql, language="sql")
        rows = run_query(sql)
        final_answer = natural_answer(q, rows)
        st.success(final_answer)
        

  
