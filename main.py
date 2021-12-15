import requests


response = requests.get('https://bank.uz/uz/currency')

print(response.text)

