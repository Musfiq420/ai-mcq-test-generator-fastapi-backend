import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

PINECONE_INDEX = "user-upload-bengali"
EMBEDDING_MODEL = "text-embedding-3-large"
LLM_MODEL = "gpt-5-nano"
