# To run program -> streamlit run Oracle_DB_chatbot.py
import os
import streamlit as st
import oracledb
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables (GROQ_API_KEY)
load_dotenv()

# Initialize chat history in session state if not already created
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit app configuration
st.set_page_config(page_title="Oracle Chatbot v1", page_icon="🤖")
st.title("Chatbot with Oracle database 23ai")
st.write("Ask questions about your database or movie quotes to get started!")

# Function to format Oracle retrieval results
def format_context(rows):
    if not rows:
        return "No retrieval context available."
    lines = []
    for row in rows:
        movie_quote, movie, movie_type, movie_year, distance = row
        lines.append(
            f"Movie: {movie}, Type: {movie_type}, Year: {movie_year}\nQuote: {movie_quote}\nDistance: {distance}"
        )
    return "\n\n".join(lines)

# Function to query Oracle Database 23ai for retrieval context using AI vector search
def get_oracle_context(search_text):
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
        conn = oracledb.connect(user="testuser1", password="testuser1", dsn="localhost:1521/freepdb1")
        cur = conn.cursor()
        cur.execute(sql, search_text=search_text)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return format_context(rows)
    except Exception as e:
        return f"Error retrieving context: {e}"

# Function to get LLM response with retrieval context within
def get_response(user_query, chat_history):
    # Retrieve additional context from Oracle using the user query
    retrieval_context = get_oracle_context(user_query)
    
    template = """
    You are a helpful assistant with access to an Oracle database containing movie quotes and related metadata.
    Use the additional context provided below to inform your answer.

    Retrieval Context:
    {retrieval_context}

    Chat History:
    {chat_history}

    User Question:
    {user_question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    # Initialize the Groq LLM client using LangChain with model "llama-3.3"
    llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")
    
    # Create the chain: prompt -> LLM -> output parser
    chain = prompt | llm | StrOutputParser()
    
    # Invoke the chain with all parameters
    return chain.stream({
        "retrieval_context": retrieval_context,
        "chat_history": chat_history,
        "user_question": user_query,
    })

# Display conversation history
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)

# Input area for user query
user_query = st.chat_input("Enter your input...")

if user_query is not None and user_query.strip() != "":
    # Append the user message to chat history
    st.session_state.chat_history.append(HumanMessage(user_query))
    with st.chat_message("Human"):
        st.markdown(user_query)
        
    # Get the AI response (streaming)
    with st.chat_message("AI"):
        ai_response = st.write_stream(get_response(user_query, st.session_state.chat_history))
    
    # Append the AI response to chat history
    st.session_state.chat_history.append(AIMessage(ai_response))
