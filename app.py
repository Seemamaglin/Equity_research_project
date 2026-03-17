import streamlit as st

# ✅ MUST BE FIRST STREAMLIT COMMAND
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
st.title("📈 News Research Tool")

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
if query and st.session_state.get("qa_chain"):
    st.text("Calling LLM... ⏳")

    try:
        response = st.session_state.qa_chain.invoke({"query": query})

        # DEBUG
        st.write("DEBUG RESPONSE:", response)

        st.subheader("Answer:")

        if "result" in response:
            st.write(response["result"])
        elif "answer" in response:
            st.write(response["answer"])
        else:
            st.write("⚠️ No answer returned")

        st.subheader("Sources:")

        if "source_documents" in response:
            for doc in response["source_documents"]:
                source = doc.metadata.get("source", "Unknown")

                if source != "Unknown":
                    st.markdown(f"[{source}]({source})")  # ✅ clickable link
                else:
                    st.write("Unknown")

    except Exception as e:
        st.error(f"Error: {e}")