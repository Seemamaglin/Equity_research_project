import requests
from bs4 import BeautifulSoup

def load_data(urls):
    documents = []

    for url in urls:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)

            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")

            text = " ".join([p.get_text() for p in paragraphs])

            if len(text) > 100:
                documents.append({
                    "text": text,
                    "source": url   # ✅ IMPORTANT
                })

        except Exception as e:
            print(e)

    return documents