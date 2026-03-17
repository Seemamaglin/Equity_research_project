from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

def split_text(data):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
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