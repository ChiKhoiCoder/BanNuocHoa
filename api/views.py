from django.http import JsonResponse
from products.models import Product
import requests


# hàm hỏi AI Ollama
def ask_ai(question):

    url = "http://localhost:11434/api/generate"

    data = {
        "model": "llama3",
        "prompt": question,
        "stream": False
    }

    try:
        r = requests.post(url, json=data)
        result = r.json()

        return result.get("response", "AI không trả lời được")

    except:
        return "Không kết nối được AI"


# API chatbot
def chat_api(request):

    question = request.GET.get("q", "").lower()

    # tìm sản phẩm theo tên
    products = Product.objects.filter(name__icontains=question)

    if products.exists():

        result = "Tôi tìm thấy các sản phẩm:\n"

        for p in products:
            result += f"{p.name} - {p.price} VND\n"

        return JsonResponse({"answer": result})

    # nếu không có sản phẩm thì hỏi AI
    ai = ask_ai(question)

    return JsonResponse({"answer": ai})