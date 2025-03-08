"""
# This is for Chat UI only:
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

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

# Conversation, this will create the convo structure, layer the texts box during chats
for message in st.session_state.chat_history:
    # human to be icon with human, check if message is human or not
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"): # st.chatmessage to select icon
            st.markdown(message.content) # this will write it out
    else:
        with st.chat_message("AI"): # st.chatmessage to select icon
            st.markdown(message.content) # this will write it out      

# Get user query if it is not an null or empty string
if user_query is not None and user_query != "":
    # First, append your user input to chat_history in the session state (as Human message)
    st.session_state.chat_history.append(HumanMessage(user_query))
    # show it in streamlit, this will show ur human input in streamlit web UI
    with st.chat_message("Human"):
        st.markdown(user_query) # markdown are the chat boxes
    
    # This will be the AI response
    with st.chat_message("AI"):
        st.markdown("IDK")

    # Just like the first human append, do the same for AI output
    st.session_state.chat_history.append(AIMessage(user_query))

# Run file -> streamlit run Test.py
"""

# Sample code with Groq (OpenAI alternative) package:
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
LLM_model="llama-3.3-70b-versatile"

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
