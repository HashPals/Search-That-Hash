import requests, json

chash = "823688dafca7393d24c871a2da98a84d8732e927"
url = "https://av5b81zg3k.execute-api.us-east-2.amazonaws.com/prod/lookup"
payload = json.dumps({"Hash": [chash]})
headers = {"Content-Type": "application/json"}
response = requests.request("GET", url, headers=headers, data=payload)
print(response.json())
