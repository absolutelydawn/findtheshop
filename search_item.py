import urllib.request
import json
import re

def get_search_item(client_id, client_secret, query):
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://openapi.naver.com/v1/search/shop?query={encoded_query}&display=100"
        request = urllib.request.Request(url)

        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)

        response = urllib.request.urlopen(request)
        response_body = response.read().decode('utf-8')

        json_data = json.loads(response_body)

        filtered_items = [item for item in json_data["items"] if item["productType"] == "1"]

        for item in filtered_items:
            clean = re.compile('<.*?>')  
            item['title'] = re.sub(clean, '', item['title'])

        filtered_json_data = {"items": filtered_items}

        with open('items.json', 'w', encoding='utf-8') as f:
            json.dump(filtered_json_data, f, ensure_ascii=False, indent=4)
        
        return filtered_json_data
    
    except Exception as e:
        print(f"Failed to retrieve search items: {e}")
        return None
