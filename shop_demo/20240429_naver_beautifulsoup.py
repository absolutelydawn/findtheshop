import requests
from bs4 import BeautifulSoup
import json 

# 크롤링할 페이지 URL
url = "https://search.shopping.naver.com/catalog/31246047618?&section=price"

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

response = requests.get(url, headers=header)

# BeautifulSoup 객체 생성
soup = BeautifulSoup(response.text, 'html.parser')

a = soup.select_one('.productList_desc__P71_8').string

print(a)


