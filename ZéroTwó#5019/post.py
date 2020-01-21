import requests
import uuid

data = {} 

url = "http://127.0.0.1:3600"+input("Url: ")
while True:
    key, value = input("key$value $ ").split("$")

    if key == "./stop" or value == "./stop":
        break
    else:
        data[key] = value

r = requests.post(url = url, data = data)

print(r.text)