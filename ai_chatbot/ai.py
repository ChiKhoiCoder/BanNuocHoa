import requests

def ask_ai(context, question):
    try:
        prompt = f"""
        Bạn là AI đọc nội dung website.

        Nội dung:
        {context}

        Câu hỏi: {question}
        Trả lời ngắn gọn, đúng nội dung.
        """

        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        return res.json().get("response", "Không có phản hồi")
    except Exception as e:
        return f"Lỗi AI: {str(e)}"