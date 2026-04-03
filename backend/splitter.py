from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
def split_text(data):
    splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # increased from 500
    chunk_overlap=100  # increased from 50
)

    docs = []

    for item in data:
        chunks = splitter.split_text(item["text"])

        for chunk in chunks:
            docs.append(
                Document(
                    page_content=chunk,
                    metadata={"source": item["source"]}  # ✅ attach source
                )
            )

    return docs