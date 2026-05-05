from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import time
from typing import List

# Load environment variables from .env file
load_dotenv()

# Get API key - try st.secrets first (Streamlit Cloud), then os.getenv (local)
def get_api_key():
    try:
        import streamlit as st
        return st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))
    except Exception:
        return os.getenv("GOOGLE_API_KEY")

# Initialize Google Gemini client
client = genai.Client(api_key=get_api_key())
EMBEDDING_MODEL = "gemini-embedding-001"  # Google's free embedding model


def embed_chunks(chunks: List[str], batch_size: int = 10) -> List[List[float]]:
    """Embeds chunks using Google Gemini's embedding model in batches."""
    embeddings = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        # Retry up to 5 times with exponential backoff for rate limits
        for attempt in range(5):
            try:
                response = client.models.embed_content(
                    model=EMBEDDING_MODEL,
                    contents=batch,
                    config=types.EmbedContentConfig(output_dimensionality=768)
                )
                for embedding in response.embeddings:
                    embeddings.append(embedding.values)
                break  # Success, exit retry loop
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    wait_time = 60 * (attempt + 1)  # 60s, 120s, 180s...
                    print(f"Rate limited. Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    raise e
        # Wait 5 seconds between batches to stay under 15 RPM
        if i + batch_size < len(chunks):
            time.sleep(5)

    return embeddings


def embed_User_query(query: str) -> List[float]:
    """Embeds a user query using Google Gemini's embedding model."""
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=query,
        config=types.EmbedContentConfig(output_dimensionality=768),
    )
    return response.embeddings[0].values
