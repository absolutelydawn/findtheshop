import urllib.request
import urllib.parse
import json
import os.path
import re

BASE_DIR = os.path.dirname(os.path.relpath("./"))
secret_file = os.path.join(BASE_DIR, 'secret.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        errorMsg = "Set the {} environment variable.".format(setting)
        return errorMsg  

client_id = get_secret("client_id")
client_secret = get_secret("client_secret")

query = input("search : ")
encoded_query = urllib.parse.quote(query)

url = f"https://openapi.naver.com/v1/search/shop?query={encoded_query}&display=100"
request = urllib.request.Request(url)

request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)

response = urllib.request.urlopen(request)
response_body = response.read().decode('utf-8')

json_data = json.loads(response_body)

filtered_items = [item for item in json_data["items"] if item["productType"] == "1"]

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

for item in filtered_items:
    item['title'] = remove_html_tags(item['title'])

filtered_json_data = {"items": filtered_items}

with open('items.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_json_data, f, ensure_ascii=False, indent=4)

print("items.json 저장 완료")