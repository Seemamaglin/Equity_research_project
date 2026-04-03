import streamlit as st

st.set_page_config(layout="wide")

import os
from dotenv import load_dotenv

from backend.loader import load_data
from backend.splitter import split_text
from backend.embeddings import get_embeddings
from backend.vector_store import create_vector_store
from backend.qa_chain import get_qa_chain

# Load env variables
load_dotenv()

# Debug API key
st.write("API KEY LOADED:", bool(os.getenv("GROQ_API_KEY")))

# Sidebar
st.sidebar.title("News Article URLs")

url1 = st.sidebar.text_input("URL 1")
url2 = st.sidebar.text_input("URL 2")
url3 = st.sidebar.text_input("URL 3")

process = st.sidebar.button("Process URLs")

# Main UI
st.title("📈 Equity Research Tool")

query = st.text_input("Question:")

# Store state
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

# Process URLs
if process:
    urls = [url1, url2, url3]
    urls = [u for u in urls if u]

    if not urls:
        st.warning("Please enter at least one URL")
    else:
        st.text("Processing articles...")

        # Load content
        texts = load_data(urls)

        st.write(f"Loaded {len(texts)} articles")

        if len(texts) == 0:
            st.error("❌ No content fetched from URLs")
            st.stop()

        # Split
        docs = split_text(texts)

        st.write(f"Created {len(docs)} chunks")

        if len(docs) == 0:
            st.error("❌ No chunks created")
            st.stop()

        # Embeddings
        embeddings = get_embeddings()

        # Vector store
        vectorstore = create_vector_store(docs, embeddings)

        # QA Chain
        st.session_state.qa_chain = get_qa_chain(vectorstore)

        st.success("Processing completed!")

# Ask question
# Ask question
if query and st.session_state.get("qa_chain"):
    st.text("Calling LLM... ⏳")

    try:
        response = st.session_state.qa_chain.invoke(query)

        st.subheader("Answer:")

        # Handle both string and dict responses
        if isinstance(response, str):
            st.write(response)

        elif isinstance(response, dict):
            if "result" in response:
                st.write(response["result"])
            elif "answer" in response:
                st.write(response["answer"])
            else:
                # Print all keys for debugging
                st.write("⚠️ Unexpected response format")
                st.write(response)

        else:
            st.write(str(response))

    except Exception as e:
        st.error(f"Error: {e}")