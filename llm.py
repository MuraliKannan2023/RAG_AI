from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

def get_secret(key):
    try:
        import streamlit as st
        return st.secrets.get(key, os.getenv(key))
    except Exception:
        return os.getenv(key)

client = Groq(api_key=get_secret("GROQ_API_KEY"))

def query_llm_with_context(query: str, context: str):
    system_content = """You are a helpful assistant for answering user queries based on provided context. 
    use the context to provide accurate and relevant answers. Do not make assumptions beyond the context provided.
    If the context does not contain enough information to answer the query, 
    let the user know that you cannot provide an answer based on the given context.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": f"Query: {query}\n\nContext:\n{context}"}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content
