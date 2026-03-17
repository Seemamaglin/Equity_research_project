import os
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq

def get_qa_chain(vectorstore):
    llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant",  # ✅ updated
    temperature=0
    
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True,
        chain_type="stuff"
    )

    return qa