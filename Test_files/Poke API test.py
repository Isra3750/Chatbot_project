# Create a streamlit chatbot using Langchain and Groq and function definition to connect to Poke API
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# create client for groq
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


