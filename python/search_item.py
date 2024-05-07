###
# 기능설명 : 네이버 openAPI를 사용한 상품 검색 및 json 파일 생성
# 작성자명 : 송한나 
# 작성일자 : 2024.05.01
###
import urllib.request
import json
import re

def get_search_item(client_id, client_secret, query):
    try:
        # 검색어 query 설정
        encoded_query = urllib.parse.quote(query)
        # 최대 100개 검색을 위한 display 설정
        url = f"https://openapi.naver.com/v1/search/shop?query={encoded_query}&display=100"
        request = urllib.request.Request(url)

        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)

        response = urllib.request.urlopen(request)
        response_body = response.read().decode('utf-8')

        json_data = json.loads(response_body)

        # 가격 비교 상품군을 위한 productType 설정
        filtered_items = [item for item in json_data["items"] if item["productType"] == "1"]

        # title에 입력되는 특수문자 제거
        for item in filtered_items:
            clean = re.compile('<.*?>')  
            item['title'] = re.sub(clean, '', item['title'])

        filtered_json_data = {"items": filtered_items}

        # 출력된 리스트를 json으로 저장 
        with open('items.json', 'w', encoding='utf-8') as f:
            json.dump(filtered_json_data, f, ensure_ascii=False, indent=4)
        
        return filtered_json_data
    
    except Exception as e:
        print(f"Failed to retrieve search items: {e}")
        return None
