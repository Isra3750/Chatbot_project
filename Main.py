# This project will be use for a database chat bot - locally ran oracle database on a docker container. Enterprise edition 19c. Will be using oracledb package and groqAPI - llama

# Will use NLP to query and push DDL towards the database. ALong with regular data modeling checks to vertify that each push is correct and fully compliance towards best pratices.
# Streamlit: Python library for building interactive, data-driven web apps quickly and easily, primarily for data science and machine learning applications.
# LangChain: framework for developing applications powered by language models, offering tools for integrating with APIs, managing memory, and handling complex workflows.

# pip install python-dotenv to read .env file 
# pip install groq for LLM API
# pip install langchain-groq for langchain usage with groq API
# Import OS to get Key from env
from dotenv import load_dotenv
from groq import Groq
import os

# pip install streamlit, Import streamlit for an UI interface
import streamlit as st

# load env variable
load_dotenv()

# Streamlit app configuration
# Set page name and icons
st.set_page_config(page_title="Database Chatbot v1", page_icon="🤖")
st.title("Oracle Database Chatbot")
st.write("Ask questions about your Oracle database or push DDL queries.")

# Get API key from env file
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# LLM Model to be used
LLM_model="llama-3.1-70b-versatile"

# Input from user
user_query = st.text_input("Enter your query:", placeholder="E.g. What is the total count of the course table?")

# Button to submit the query
if st.button("Submit"):
    if user_query is not None and user_query != "":  # Check if the input is not empty
        try:
            # Send the user query to the Groq LLM
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": user_query,
                    }
                ],
                model=LLM_model,
            )
            # Display the response
            response = chat_completion.choices[0].message.content
            st.success("Response:")
            st.write(response)
        except Exception as e:
            st.error("An error occurred while processing your query.")
            st.write(f"Error details: {e}")
    else:
        st.warning("Please enter a valid query.")

# Additional features can be added here for DDL verification and modeling checks
st.write(f"Note: No database is connected as of 12/5/2024. Current LLM model: {LLM_model}")

# Run file -> streamlit run Main.py