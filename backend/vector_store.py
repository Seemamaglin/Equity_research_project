from langchain.vectorstores import FAISS

def create_vector_store(docs, embeddings):
    return FAISS.from_documents(docs, embeddings)