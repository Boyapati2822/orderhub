import httpx

response = httpx.get("http://127.0.0.1:8000/")
post_response = httpx.post("http://127.0.0.1:8000/", content=b"hi")
print(post_response.status_code)
print(post_response.text)

print(response.status_code)
print(response.text)
