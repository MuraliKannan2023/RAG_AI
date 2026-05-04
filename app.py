import streamlit as st
from pdfreader import read_pdf
from chunker import chunk_pages
from embedder import embed_chunks, embed_User_query
from vectorstore import store_in_pinecone, search_in_pinecone
from llm import query_llm_with_context
import os
import tempfile

# Page configuration
st.set_page_config(
    page_title="RAG AI - Document Assistant",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 RAG AI — Document Assistant")
st.caption("Upload a PDF, index it, and ask questions!")

# Sidebar for PDF upload & indexing
with st.sidebar:
    st.header("📄 Document Management")

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file:
        # Save uploaded file to a temp location
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded: {uploaded_file.name}")

        # Index button
        if st.button("📥 Index Document", use_container_width=True):
            with st.spinner("Processing PDF..."):
                # Step 1: Read PDF
                st.info("📖 Reading PDF...")
                pages = read_pdf(temp_path)
                st.write(f"Pages extracted: {len(pages)}")

                # Step 2: Chunk
                st.info("✂️ Chunking text...")
                chunks = chunk_pages(pages, chunk_size=900, chunk_overlap=150)
                st.write(f"Chunks created: {len(chunks)}")

                # Step 3: Embed
                st.info("🔢 Creating embeddings...")
                embedded_chunks = embed_chunks(chunks)
                st.write(f"Embeddings created: {len(embedded_chunks)}")

                # Step 4: Store
                st.info("💾 Storing in Pinecone...")
                store_in_pinecone(chunks, embedded_chunks, namespace="")

                st.success("✅ Document indexed successfully!")
                st.session_state["indexed"] = True

    st.divider()
    st.markdown("### ⚙️ Tech Stack")
    st.markdown("- **Embeddings:** Gemini")
    st.markdown("- **Vector DB:** Pinecone")
    st.markdown("- **LLM:** Groq + Llama 3.3")
    st.markdown("- **Cost:** Free!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your document..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Step 1: Embed the query
            query_vector = embed_User_query(prompt)

            # Step 2: Search Pinecone
            matched_chunks = search_in_pinecone(query_vector)

            # Step 3: Generate answer
            context = "\n\n".join(matched_chunks)
            response = query_llm_with_context(prompt, context)

            st.markdown(response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
