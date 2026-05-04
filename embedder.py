from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import time
from typing import List

# Load environment variables from .env file
load_dotenv()

# Initialize Google Gemini client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
EMBEDDING_MODEL = "gemini-embedding-001"  # Google's free embedding model


def embed_chunks(chunks: List[str], batch_size: int = 100) -> List[List[float]]:
    """Embeds chunks using Google Gemini's embedding model in batches."""
    embeddings = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=batch,
            config=types.EmbedContentConfig(output_dimensionality=768)
        )
        for embedding in response.embeddings:
            embeddings.append(embedding.values)
        # Rate limit: wait between batches
        if i + batch_size < len(chunks):
            time.sleep(1)

    return embeddings


def embed_User_query(query: str) -> List[float]:
    """Embeds a user query using Google Gemini's embedding model."""
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=query,
        config=types.EmbedContentConfig(output_dimensionality=768),
    )
    return response.embeddings[0].values
