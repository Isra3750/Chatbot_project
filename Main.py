# This project will be use for a database chat bot - locally ran oracle database on a docker container. Enterprise edition 19c. Will be using oracledb package and groqAPI - llama
# Will use NLP to query and push DDL towards the database. ALong with regular data modeling checks to vertify that each push is correct and fully compliance towards best pratices.
# Streamlit and langchain is to be used somewhere...

# pip install python-dotenv to read .env file 
# pip install groq for LLM API
# Import OS to get Key from env
from dotenv import load_dotenv
from groq import Groq
import os

# load env variable
load_dotenv()

# Get API key from env file
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Create your prompt and select model
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama-3.1-70b-versatile",
)

print(chat_completion.choices[0].message.content)