import requests

def ask_ai(question):
    try:
        # dùng model nhẹ
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": f"Trả lời bằng tiếng Việt: {question}",
                "stream": False
            }
        )

        data = r.json()
        answer = data.get("response", "Không có câu trả lời")

        # nếu có tiếng Anh thì dịch
        if any(c.isascii() for c in answer[:50]):
            r2 = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "tinyllama",
                    "prompt": f"Dịch sang tiếng Việt:\n{answer}",
                    "stream": False
                }
            )
            return r2.json().get("response", answer)

        return answer

    except Exception as e:
        return f"Lỗi: {str(e)}"