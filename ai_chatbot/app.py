from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from crawl import get_text
from ai import ask_ai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/chat")
def chat(q: str):
    context = get_text()

    if not context:
        return {"answer": "Không đọc được nội dung web"}

    answer = ask_ai(context, q)
    return {"answer": answer}