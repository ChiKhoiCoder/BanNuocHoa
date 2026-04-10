import requests

def verify_fix():
    urls = [
        "http://127.0.0.1:8000/",
        "http://127.0.0.1:8000/products/"
    ]
    for url in urls:
        print(f"\nChecking: {url}")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                content = response.text
                if "{% include" in content:
                    print(f"FAILURE: Raw template tag found in {url}!")
                else:
                    print(f"SUCCESS: No raw template tags found in {url}.")
                
                if "KHƠI NGUỒN BẢN NGÃ" in content or "BỘ SƯU TẬP DI SẢN" in content:
                    print("SUCCESS: Hero title found.")
                else:
                    print("FAILURE: Hero title not found.")
            else:
                print(f"Server returned status code {response.status_code} for {url}")
        except Exception as e:
            print(f"Error connecting to {url}: {e}")

if __name__ == "__main__":
    verify_fix()
