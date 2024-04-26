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
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient
import json
from pyvirtualdisplay import Display
from datetime import datetime
import sys

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

# 사용자 정의 대기 조건 함수
def attribute_to_be(locator, attribute, value):
    def predicate(driver):
        element = driver.find_element(*locator)
        return element.get_attribute(attribute) == value
    return predicate

# 리뷰 수집
# 로직 수정 : "쇼핑몰리뷰"탭 클릭 정확히하기..
def collectReviews(product_id):
    url = f"https://search.shopping.naver.com/catalog/{product_id}"
    try:
        driver.get(url)
        review_tab_locator = (By.XPATH, '/html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[1]/ul/li[3]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(review_tab_locator))
        review_tab = driver.find_element(*review_tab_locator)
        if review_tab.get_attribute('aria-selected') == 'false':
            review_tab.click()
            WebDriverWait(driver, 10).until(attribute_to_be(review_tab_locator, 'aria-selected', 'true'))
        scrollDown(driver)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        reviews = [p.text for p in soup.select('div.reviewItems_review__DqLYb div.reviewItems_review_text__dq0kE p.reviewItems_text__XrSSf')]
        reviews_json = json.dumps(reviews)
        saveDatabase(product_id, reviews_json)
    except Exception as e:
        print(f"Failed to process URL for product ID {product_id}: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        product_id_input = sys.argv[1]
        collectReviews(product_id_input)
    else:
        print("Insufficient arguments provided. Please provide Product ID.")