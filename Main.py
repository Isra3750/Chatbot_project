# This project will be use for a database chat bot - locally ran oracle database on a docker container. Enterprise edition 19c. Will be using oracledb package and groqAPI - llama

# Will use NLP to query and push DDL towards the database. ALong with regular data modeling checks to vertify that each push is correct and fully compliance towards best pratices.
# Streamlit: Python library for building interactive, data-driven web apps quickly and easily, primarily for data science and machine learning applications.
# LangChain: framework for developing applications powered by language models, offering tools for integrating with APIs, managing memory, and handling complex workflows.

# pip install python-dotenv to read .env file 
# pip install groq for LLM API
# pip install langchain-groq for langchain usage with groq API
# Import OS to get Key from env
from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# pip install streamlit, Import streamlit for an UI interface
import streamlit as st
import os

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


###This is written third (for LLM response and streaming)

# Get response -> Use LLM to get response
def get_response(user_query, chat_history):
    # Template 
    template = """
    You are a helpful assistant. Answer the following questions considering the history of the conversation:

    Chat history: {chat_history}

    User question: {user_question}
    """
    # Create prompt template - from langchain core 
    prompt = ChatPromptTemplate.from_template(template)

    # lang chain groq for LLM model API, api key is in env
    llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile") 
    
    # Create chain which output LLM response via StrOutputParser, which is then return
    chain = prompt | llm | StrOutputParser()
    
    # Invoke your chain, with the 2 arg from this function, StrOutputParser will output LLM response
    # use chain.invoke for one time output, chain.stream for generator output (one at a time output)
    return chain.stream({
        "chat_history": chat_history,
        "user_question": user_query,
    })

###This is written second (for session history)
# Conversation, this will create the convo structure, layer the texts box during chats
for message in st.session_state.chat_history:
    # human to be icon with human, check if message is human or not
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"): # st.chatmessage to select icon
            st.markdown(message.content) # this will write it out
    else:
        with st.chat_message("AI"): # st.chatmessage to select icon
            st.markdown(message.content) # this will write it out    

###This is written first (User query), ai response was using place holder before this
# Create the message box with default message
user_query = st.chat_input("Enter your input...")  

# Get user query if it is not an null or empty string
if user_query is not None and user_query != "":
    # First, append your user input to chat_history in the session state (as Human message)
    st.session_state.chat_history.append(HumanMessage(user_query))
    # show it in streamlit, this will show ur human input in streamlit web UI
    with st.chat_message("Human"):
        st.markdown(user_query) # markdown are the chat boxes
    
    # This will be the AI response
    with st.chat_message("AI"):
        # write it out with markdown (with invoke in function), or write_stream (with stream in function)
        ai_response = st.write_stream(get_response(user_query, st.session_state.chat_history))

    # Just like the first human append, do the same for AI output, but with AI message
    st.session_state.chat_history.append(AIMessage(ai_response))

# Run file -> streamlit run Main.py