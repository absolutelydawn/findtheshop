import urllib.request
import urllib.parse
import json
import subprocess


client_id = ""
client_secret = ""

query = input("search : ")
encoded_query = urllib.parse.quote(query)

url = f"https://openapi.naver.com/v1/search/shop?query={encoded_query}&display=100"
request = urllib.request.Request(url)

request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)

response = urllib.request.urlopen(request)
response_body = response.read().decode('utf-8')

json_data = json.loads(response_body)
# 가격비교 상품군 productType = 1
filtered_items = [item for item in json_data["items"] if item["productType"] == "1"]
filtered_json_data = {"items": filtered_items}

with open('db.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_json_data, f, ensure_ascii=False, indent=4)

print("Data saved to db.json")

subprocess.run(["./server.sh"], shell=True)
