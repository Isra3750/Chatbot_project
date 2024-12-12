import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# app config
st.set_page_config(page_title="Streamlit Chatbot", page_icon="🤖")
st.title("Chatbot")

def get_response(user_query, chat_history):

    template = """
    You are a helpful assistant. Answer the following questions considering the history of the conversation:

    Chat history: {chat_history}

    User question: {user_question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatGroq(model_name="llama-3.3-70b-versatile")  # Replace OpenAI LLM with Groq LLM
        
    chain = prompt | llm | StrOutputParser()
    
    return chain.stream({
        "chat_history": chat_history,
        "user_question": user_query,
    })

# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am a bot. How can I help you?"),
    ]

# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# user input
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = st.write_stream(get_response(user_query, st.session_state.chat_history))

    st.session_state.chat_history.append(AIMessage(content=response))

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

    
"""
