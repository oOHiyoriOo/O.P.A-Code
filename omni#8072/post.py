import requests


url = "http://127.0.0.1:8080"
data = {
    "user":str(input("user: ")),
    "data":str(input("data: "))

    } 

r = requests.post(url = url, data = data)

print(r.text)