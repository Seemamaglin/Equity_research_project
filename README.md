# 📈 News Research Tool

An AI-powered web application that helps users extract insights from multiple news articles using LLMs and vector search.

---

## 🚀 Features

- 🔗 Input multiple news article URLs
- 📄 Extract and process article content
- 🧠 Generate embeddings using HuggingFace
- 🔍 Store data using FAISS vector database
- 🤖 Ask questions using LLM (Groq - LLaMA 3.1)
- 📊 Get summarized answers with sources
- 🔗 Clickable source links

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Groq API (LLM)
- HuggingFace Embeddings
- FAISS (Vector Store)
- BeautifulSoup (Web Scraping)

## How to run the project
1.python -m venv venv
2.venv\Scripts\activate
3.pip install -r requirements.txt
4.GROQ_API_KEY=your_api_key_here
5.python -m streamlit run app.py
