import streamlit as st
import pandas as pd
import sqlite3

st.title("AI Data Analyst")

file = st.file_uploader("Upload CSV")

if file:
    df = pd.read_csv(file)
    st.write(df.head())

    conn = sqlite3.connect("data.db")
    df.to_sql("emails", conn, if_exists="replace", index=False)

    question = st.text_input("Ask anything")

    if question:
        question = question.lower()

    # Count spam
    if "spam" in question and ("how many" in question or "count" in question):
        sql = "SELECT COUNT(*) as total_spam FROM emails WHERE Category='spam'"

    # Count ham
    elif "ham" in question and ("how many" in question or "count" in question):
        sql = "SELECT COUNT(*) as total_ham FROM emails WHERE Category='ham'"

    # Show spam
    elif "show spam" in question:
        sql = "SELECT * FROM emails WHERE Category='spam'"

    # Show ham
    elif "show ham" in question:
        sql = "SELECT * FROM emails WHERE Category='ham'"

    # Search keyword
    elif "search" in question or "containing" in question:
        word = question.replace("search", "").replace("containing", "").strip()
        sql = f"SELECT * FROM emails WHERE Message LIKE '%{word}%'"

    else:
        sql = "SELECT * FROM emails LIMIT 5"

    st.write("SQL Query:", sql)

    result = pd.read_sql(sql, conn)
    st.write(result)