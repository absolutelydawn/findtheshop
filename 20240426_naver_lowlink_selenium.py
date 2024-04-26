from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import json
from pyvirtualdisplay import Display 
from datetime import datetime

###
# for Linux : Linux 환경에서 selenium 실행 시 필요한 옵션
display = Display(visible=0, size=(1920, 1080))
display.start()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=chrome_options)
###  

# def scrollDown(driver):
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     while True:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(2)
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             break
#         last_height = new_height


# def collectReviews(product_id):
#     url = f"https://search.shopping.naver.com/catalog/{product_id}"
#     try:
#         driver.get(url)
#         WebDriverWait(driver, 1000).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.floatingTab_on__2FzR0 a[aria-selected="true"] strong'))
#         )
#         review_tab = driver.find_element(By.CSS_SELECTOR, 'li.floatingTab_on__2FzR0 a[aria-selected="true"] strong')
#         if review_tab.text == "쇼핑몰리뷰":
#             review_tab.click()
#         scrollDown(driver)
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         reviews = [p.text for p in soup.select('div.reviewItems_review__DqLYb div.reviewItems_review_text__dq0kE p.reviewItems_text__XrSSf')]
#         reviews_json = json.dumps(reviews)
#     except Exception as e:
#         print(f"Failed to process URL for product ID {product_id}: {e}")


# JSON 파일에서 데이터 읽어오기
with open('items.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# 최저가 링크 수집 함수
def get_lowest_price_link(url):
    try:
        driver.get(url)
        # 최저가 링크 기다리기 및 클릭
        lowest_price_link = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/div/div[2]/div[2]/table/tbody/tr[1]/td[2]/a'))
        )
        return lowest_price_link.get_attribute('href')
    except Exception as e:
        print(f"Failed to get lowest price link for URL {url}: {e}")
        return None

for item in json_data["items"]:
    product_id = item["productId"]
    print("Product ID:", product_id)
    link = get_lowest_price_link(product_id)
    print(link)

# WebDriver 종료
driver.quit()