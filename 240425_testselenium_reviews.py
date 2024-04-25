#!/usr/bin/env python
###
# 리뷰 수집하여 mongodb에 입력 :
# 네이버 openAPI로 받아온 productId 속성과 검색어(query)를 기준으로 productId당 제품리뷰를 수집한다.
# 작성자명 : 장다은
# 작성일자 : 240425
# 기타사항 : 
# 개선 ) 별점, 작성일자 스크래핑 로직 추가할것, 작성일자기준으로 sorting하여 스크래핑할것, 
#        리뷰개수 최대 100개로 설정하여 스크래핑할것, productId를 MongoDB fts DB > item collection 에서 받아오도록 수정
###

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient
import json
from pyvirtualdisplay import Display # Linux 환경에서 selenium 실행 시 필요 패키지
from datetime import datetime

###
# for Linux : Linux 환경에서 selenium 실행 시 필요한 옵션
display = Display(visible=0, size=(1920, 1080))
display.start()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=chrome_options)
###

# MongoDB 클라이언트 초기화 및 데이터베이스 연결
client = MongoClient('mongodb://192.168.1.162:27017/')
db = client['fts'] # MongoDB DB명 : fts(findtheshop 약자)
reviews_collection = db['reviews'] # MongoDB Collection명

def saveDatabase(product_id, reviews_json):
    reviews_data = json.loads(reviews_json)
    for i, review in enumerate(reviews_data):
        document = {
            "productId": product_id, # 상품당 id값
            "contents": review, # 리뷰 본문
            "rank": i + 1,  # 리뷰당 별점(추후 스크래핑로직 추가할것)
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 작성일자(추후 스크래핑로직 추가할것)
        }
        result = reviews_collection.insert_one(document)
        print(f"Added review to MongoDB with _id: {result.inserted_id}")

def scrollDown(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# 리뷰 수집
def collectReviews(product_id, query):
    url = f"https://search.shopping.naver.com/catalog/{product_id}?query={query}"
    try:
        driver.get(url)
        WebDriverWait(driver, 1000).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.floatingTab_on__2FzR0 a[aria-selected="true"] strong'))
        )
        review_tab = driver.find_element(By.CSS_SELECTOR, 'li.floatingTab_on__2FzR0 a[aria-selected="true"] strong')
        if review_tab.text == "쇼핑몰리뷰":
            review_tab.click()
        scrollDown(driver)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        reviews = [p.text for p in soup.select('div.reviewItems_review__DqLYb div.reviewItems_review_text__dq0kE p.reviewItems_text__XrSSf')]
        reviews_json = json.dumps(reviews)
        saveDatabase(product_id, reviews_json)
    except Exception as e:
        print(f"Failed to process URL for product ID {product_id}: {e}")

# 사용자 입력 받기 : 
product_id_input = input("Enter Product ID: ")
query_input = input("Enter Query: ")

# 리뷰 수집 및 결과 출력
collectReviews(product_id_input, query_input)

# WebDriver 종료
driver.quit()
