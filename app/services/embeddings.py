# app/services/embeddings.py
from langchain_openai import OpenAIEmbeddings
from app.config import OPENAI_API_KEY

# Initialize the LangChain Embeddings object
embeddings = OpenAIEmbeddings(
    openai_api_key=OPENAI_API_KEY,
    model="text-embedding-3-large" 
)
