from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from app.config import PINECONE_API_KEY
from app.services.embeddings import embeddings 

pc = Pinecone(api_key=PINECONE_API_KEY)

INDEX_NAME = "study-assistant-context-demo"

index = pc.Index(INDEX_NAME)


# Initialize the LangChain Vector Store
# This links your Pinecone index with your Embeddings model
vector_store = PineconeVectorStore(
    index=index, 
    embedding=embeddings, # Ensure this matches your Pinecone metadata field
    text_key="text"
)


def add_documents(chunks: list[str]):
    """
    This replaces upsert_chunks.
    It automatically embeds the text and uploads to Pinecone.
    """
    # LangChain handles the embedding and upsert logic internally
    vector_store.add_texts(texts=chunks)

def retrieve_context(query: str, top_k: int = 5):
    """
    This replaces your manual retrieve_context logic.
    It performs similarity search.
    """
    results = vector_store.similarity_search(query, k=top_k)
    # Combine the page content of the results
    return "\n\n".join([doc.page_content for doc in results])
