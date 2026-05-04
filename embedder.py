from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from typing import List

# Load environment variables from .env file
load_dotenv()

# Initialize Google Gemini client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
EMBEDDING_MODEL = "gemini-embedding-001"  # Google's free embedding model


def embed_chunks(chunks: List[str]) -> List[List[float]]:
    """Embeds chunks using Google Gemini's embedding model."""
    embeddings = []
    for chunk in chunks:
        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=chunk,
            config=types.EmbedContentConfig(output_dimensionality=768)
        )
        embeddings.append(response.embeddings[0].values)

    return embeddings


def embed_User_query(query: str) -> List[float]:
    """Embeds a user query using Google Gemini's embedding model."""
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=query,
        config=types.EmbedContentConfig(output_dimensionality=768),
    )
    return response.embeddings[0].values
