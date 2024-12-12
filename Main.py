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

# Create chat history section in streamlit, if not created before - which it is not
# st.session_state is object that keep all var (including old ones)
if "chat_history" not in st.session_state:
    # Create chat_history as empty array in your session_state
    # this will log messages
    st.session_state.chat_history = []

# Streamlit app configuration
# Set page name and icons
st.set_page_config(page_title="Streaming Chatbot v1", page_icon="🤖")
st.title("Streaming Chatbot")
st.write("Ask questions about your question to get started!")

# Create the message box with default message
user_query = st.chat_input("Enter your input...")

# Get user query if it is not an null or empty string
if user_query is not None and user_query != "":
    # First, append your user input to chat_history in the session state
    st.session_state.chat_history.append(user_query)

# Run file -> streamlit run Main.py