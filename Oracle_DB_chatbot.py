# streamlit run Oracle_DB_chatbot.py
import os
import streamlit as st
import oracledb
from groq import Groq
from dotenv import load_dotenv

# Load environment variables (e.g. GROQ_API_KEY)
load_dotenv()

# Streamlit app configuration
st.set_page_config(page_title="Database Chatbot v1", page_icon="🤖")
st.title("Oracle Database Chatbot")
st.write("Ask questions about your Oracle database or push DDL queries.")

# Initialize the Groq client (using the Groq API key from environment variables)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
LLM_model="llama-3.3-70b-versatile"

# Function to query Oracle Database 23ai for vector search context
def query_oracle(search_text):
    sql = """
        SELECT movie_quote, movie, movie_type, movie_year, distance
        FROM (
             SELECT movie_quote, movie, movie_type, movie_year, 
                    vector_distance(
                        movie_quote_vector,
                        vector_embedding(all_minilm_l12_v2 USING :search_text as data)
                    ) AS distance
             FROM movie_quotes
             ORDER BY distance
        ) t
        WHERE ROWNUM <= 3
    """
    try:
        # Connect to Oracle Database running in Docker
        conn = oracledb.connect(user="testuser1", password="testuser1", dsn="localhost:1521/freepdb1")
        cur = conn.cursor()
        cur.execute(sql, search_text=search_text)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"Error querying Oracle DB: {e}")
        return []

# Helper function to format the retrieved rows into a context string
def format_context(rows):
    # Each row is expected as (movie_quote, movie, movie_type, movie_year, distance)
    context_lines = []
    for row in rows:
        movie_quote, movie, movie_type, movie_year, distance = row
        context_lines.append(
            f"Movie: {movie}\nType: {movie_type}\nYear: {movie_year}\nQuote: {movie_quote}\nDistance: {distance}"
        )
    return "\n\n".join(context_lines)

# Get user input from the Streamlit UI
user_query = st.text_input("Enter your query:", placeholder="E.g. Tell me about war films")

if st.button("Submit"):
    if user_query and user_query.strip():
        # Retrieve context from Oracle DB based on the user's query
        rows = query_oracle(user_query)
        context = format_context(rows)
        
        # Build the prompt for the LLM by including the retrieval context
        prompt = (
            "Here is some context from the Oracle database:\n\n"
            f"{context}\n\n"
            "Using the above context, answer the following query:\n"
            f"{user_query}"
        )
        
        try:
            # Send the prompt to the Groq LLM
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=LLM_model,
            )
            response = chat_completion.choices[0].message.content
            st.success("Response:")
            st.write(response)
        except Exception as e:
            st.error("An error occurred while processing your query.")
            st.write(f"Error details: {e}")
    else:
        st.warning("Please enter a valid query.")

st.write("Note: This example connects to Oracle Database 23ai running in Docker (DSN: localhost:1521/freepdb1).")
