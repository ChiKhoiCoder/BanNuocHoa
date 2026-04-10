from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
import sys
import os

# Đảm bảo có thể import từ thư mục hiện tại
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai import ask_ai
from crawl import crawl_and_save

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/chat")
def chat(q: str, background_tasks: BackgroundTasks, url: str = None):
    if url and url.startswith("http"):
        if "127.0.0.1" in url or "localhost" in url:
             background_tasks.add_task(crawl_and_save, url)
    
    answer = ask_ai(q)
    return {"answer": answer}

@app.get("/summary")
def get_summary(url: str):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        
        # Thử lấy thông tin sản phẩm
        name = soup.find("h1").text.strip() if soup.find("h1") else "Nội dung"
        price = ""
        # Thử tìm giá
        price_tag = soup.select_one(".price-main, .price, .text-primary.fs-3")
        if price_tag:
            price = price_tag.text.strip()
            
        desc = ""
        # Thử tìm mô tả
        desc_tag = soup.select_one(".product-description, .mt-4 p, main p")
        if desc_tag:
            desc = desc_tag.text.strip()[:300] + "..."
            
        return {
            "name": name,
            "price": price,
            "description": desc,
            "url": url
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/crawl")
def trigger_crawl(url: str):
    result = crawl_and_save(url)
    return {"message": result}