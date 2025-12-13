import requests

try:
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    print("status code:", response.status_code)
    print("response text:\n", response.text)
    data = response.json()
    print("resp data:\n ", data)
except:
    print("Some error occured.")