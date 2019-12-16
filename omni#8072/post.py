import requests

url = "http://127.0.0.1:8080"
data = {
    "user":"PI",
    "data":str(input("Data: "))

    } 

r = requests.post(url = url, data = data)