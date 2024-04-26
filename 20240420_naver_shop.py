import urllib.request
import urllib.parse
import json
import subprocess
import os.path 
import re

BASE_DIR = os.path.dirname((os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, '../secret.json')

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

# API 요청 URL 구성
url = f"https://openapi.naver.com/v1/search/shop?query={encoded_query}&display=20"
request = urllib.request.Request(url)

# 네이버 API에 요청 헤더 추가
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)

# API 응답 받아오기
response = urllib.request.urlopen(request)
response_body = response.read().decode('utf-8')

# JSON 데이터 파싱
json_data = json.loads(response_body)

# 가격비교 상품군 productType = 1 필터링
filtered_items = [item for item in json_data["items"] if item["productType"] == "1"]

# HTML 태그 제거 함수
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# HTML 태그 제거 및 필터링된 아이템을 새로운 JSON 데이터로 저장
for item in filtered_items:
    item['title'] = remove_html_tags(item['title'])

filtered_json_data = {"items": filtered_items}

# JSON 파일로 저장
with open('items.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_json_data, f, ensure_ascii=False, indent=4)

#subprocess.run(["./server.sh"], shell=True)
