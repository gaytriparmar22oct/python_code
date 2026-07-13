import requests

response = requests.get("https://www.google.com")

print(response.status_code)


if response.status_code==200:
    print("Request successful")
else:
    print("Request failed")