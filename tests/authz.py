import requests

url = 'http://localhost:8060/token/'

data = {"chicken":"bannans"}

x = requests.post(url, data)

print(x)