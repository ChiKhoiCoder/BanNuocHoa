import requests
from bs4 import BeautifulSoup
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

def crawl_and_save(url="http://127.0.0.1:8000/"):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        
        # Lấy tiêu đề và nội dung chính
        title = soup.title.string if soup.title else ""
        text = soup.get_text(separator=' ', strip=True)
        
        full_text = f"Tiêu đề: {title}\nNội dung: {text}"

        splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

        chunks = splitter.split_text(full_text)

        embeddings = OllamaEmbeddings(model="nomic-embed-text")

        db = Chroma.from_texts(
            chunks,
            embeddings,
            persist_directory="./chroma"
        )

        return f"Đã lưu dữ liệu từ {url} vào database"
    except Exception as e:
        return f"Lỗi khi crawl {url}: {str(e)}"

if __name__ == "__main__":
    print(crawl_and_save())