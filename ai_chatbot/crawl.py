import requests
from bs4 import BeautifulSoup

URL = "http://127.0.0.1:8000/"

def get_text():
    try:
        res = requests.get(URL, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")

        text = soup.get_text(separator=" ", strip=True)

        return text[:8000]
    except Exception as e:
        print("Lỗi crawl:", e)
        return ""