import requests
import asyncio
import concurrent.futures


headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOiIxIiwidXNlcnJvbGUiOiIxIiwidXNlcm5hbWUiOiJBZG1pbmlzdHJhdG9yIiwidXNlcmVtYWlsIjoic3VwcG9ydEBzb25saW5lLnVzIiwiYWNjZXNzbG9naWQiOjF9.ohZpZukrNe_tJ75Ha12vpVVUgnfIcuDXuFQlBwJzqf0"}

# async def send_request(program_id):
#     print("Program_id",program_id)
#     req = requests.get(f"http://127.0.0.1:8000/{program_id}", headers=headers)
#     print("Status Code",req.status_code)
#     if req.status_code != 200:
#         print(req.content)
#     print("\n")

# async def loop_func():
#     for i in range(1,11):
#         await send_request(i)
#     # assert requests.get(f"http://127.0.0.1:8000/{i}", headers=headers)
    
# # loop_func()
# asyncio.run(loop_func())

def send_request(url):
    req = requests.get(url, headers=headers)
    if req.status_code != 200:
        return url, req.status_code, req.content
    return url, req.status_code

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    futures = []
    urls = [f"http://127.0.0.1:8000/{program_id}" for program_id in range(1,11) ]*30
    print(len(urls))
    for url in urls:
        futures.append(executor.submit(send_request, url=url))

    for future in concurrent.futures.as_completed(futures):
        print(future.result())