from pyvirtualdisplay import Display
import pandas as pd
import urllib.request
import urllib.parse
import json
import re
######################
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
###
# for Linux : Linux 환경에서 selenium 실행 시 필요한 옵션
display = Display(visible=0, size=(1920, 1080))
display.start()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=chrome_options)
###

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
    url = f"https://search.shopping.naver.com/catalog/{product_id}"
    print("Product ID:", product_id)
    print("Shopping Link:", url)
    link = get_lowest_price_link(url)
    print(link)

# WebDriver 종료
driver.quit()

