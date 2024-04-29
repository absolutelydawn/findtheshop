#!/usr/bin/env python
###
# 리뷰 수집하여 mongoDB에 입력 + .sh으로 fastAPI와 연동
# 작성자명 : 장다은
# 작성일자 : 240429
# url 수정 : section=review 해서 리뷰탭 바로이동
# 최신순으로 수집, max 100개리뷰, 글자수 50자 이상
# date > 작성일자 수집 수정완료
# rank > 평점 수집 수정완료

# 개선사항 : coding convention 준수하기
# 만약 쇼핑몰리뷰 탭이 없으면 스크래핑을 중단하고 콘솔에 "No reviews" 출력하기
# 만약 50글자 이상의 리뷰가 없으면 스크래핑 중단하고 콘솔에 "No reviews_No 50" 출력하기
# 100개 미만이라도 리뷰 수집이 끝나면 스크래핑 바로 중단

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
import sys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display

# Linux 환경에서 selenium 실행 시 필요한 옵션
display = Display(visible=0, size=(1920, 1080))
display.start()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=chrome_options)

# MongoDB 연결 설정
client = MongoClient('mongodb://192.168.1.162:27017/')
db = client['fts']
reviews_collection = db['reviews']

# 리뷰 저장 함수
def saveDatabase(product_id, reviews):
    for i, (review_text, review_date, rank) in enumerate(reviews):
        document = {
            "productId": product_id,
            "contents": review_text,
            "date": review_date,
            "rank": rank
        }
        reviews_collection.insert_one(document)
        print(f"Added review with _id: {document['_id']}")

# 스크롤 다운 함수
def scrollDown(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 스크롤 대기
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# 리뷰 수집 함수 : Selenium 실행 후 BeautifulSoup으로 스크래핑
# 최신순으로 100개까지 수집, 글자수 50자 이상인것만 수집
def collectReviews(product_id):
    start_time = datetime.now()  # 수집 시작 시간 기록
    url = f"https://search.shopping.naver.com/catalog/{product_id}?section=review"
    driver.get(url)

    try:
        # '최신순' 정렬 버튼 클릭
        sort_button_locator = (By.CSS_SELECTOR, "a[data-nclick='N=a:rev.rec']")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(sort_button_locator))
        driver.find_element(*sort_button_locator).click()

        reviews_collected = []
        page_number = 1

        while len(reviews_collected) < 100:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.reviewItems_list_review__q726A p.reviewItems_text__XrSSf"))
            )
            scrollDown(driver)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            review_blocks = soup.select("ul.reviewItems_list_review__q726A li")

            for block in review_blocks:
                review_text = block.select_one("p.reviewItems_text__XrSSf").get_text().strip()
                review_date = block.select_one("div.reviewItems_etc_area__3VUjt span.reviewItems_etc__9ej69:nth-of-type(4)").get_text().strip()
                rank = block.select_one("div.reviewItems_etc_area__3VUjt span.reviewItems_average__0kLWX").get_text().strip()
                rank = int(rank.replace("평점", ""))

                if len(review_text) >= 50:
                    reviews_collected.append((review_text, review_date, rank))
                    if len(reviews_collected) % 10 == 0:
                        print(f"{len(reviews_collected)}개의 리뷰 수집중...")

            if len(reviews_collected) >= 100:
                print("100개의 리뷰 수집 완료.")
                break

            # 다음 페이지 버튼 클릭 처리
            page_number += 1
            next_page_locator = (By.CSS_SELECTOR, f"a[data-nclick='N=a:rev.page,r:{page_number}']")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(next_page_locator))
            next_page_button = driver.find_element(*next_page_locator)
            driver.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
            driver.execute_script("arguments[0].click();", next_page_button)
            time.sleep(2)  # 페이지 로드 대기

        saveDatabase(product_id, reviews_collected)
        end_time = datetime.now()  # 수집 종료 시간 기록
        print(f"수집 완료. 총 소요 시간: {end_time - start_time}")

    except Exception as e:
        print(f"An exception occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        product_id_input = sys.argv[1]
        collectReviews(product_id_input)
    else:
        print("Insufficient arguments provided. Please provide Product ID.")
