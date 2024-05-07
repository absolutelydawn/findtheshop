###
# 기능설명 : 최저가 링크 크롤링을 위한 함수 생성
# 작성자명 : 송한나 
# 작성일자 : 2024.05.01
###

from selenium import webdriver
from pyvirtualdisplay import Display 
import time
from bs4 import BeautifulSoup


def get_lowest_price(url, productId):
    try: 
        # for Linux : Linux 환경에서 selenium 실행 시 필요한 옵션
        ###
        display = Display(visible=0, size=(1920, 1080))
        display.start()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(1)
        ###

        # BeautifulSoup을 이용한 크롤링 화면 설정
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        result = []

        # 최저가 정보 최대 5개까지 크롤링
        for i in range(1, 6):
            # 최저가 리스트 링크 크롤링
            link_selector = f"#section_price > div.productList_seller_wrap__FZtUS > ul  li:nth-child({i}) > div > div.productList_price__2eGt4 > a"
            lowlink_list_link = soup.select_one(link_selector)
            # 최저가 리스트 가격 크롤링
            price_selector = f"#section_price > div.productList_seller_wrap__FZtUS > ul > li:nth-child({i}) > div > div.productList_price__2eGt4 > a > span > em"
            lowlink_list_price = soup.select_one(price_selector)
            # 최저가 리스트 배송비 크롤링
            delivery_selector = f"#section_price > div.productList_seller_wrap__FZtUS > ul > li:nth-child({i}) > div > div.productList_price__2eGt4 > div.productList_delivery__WwSwL"
            lowlink_list_delivery = soup.select_one(delivery_selector)

            # 사용하지 않는 문자열 제거
            if lowlink_list_link:
                lowlinks_href = lowlink_list_link.attrs['href']
                lowlinks_price = lowlink_list_price.get_text().strip().replace(",", "")
                lowlinks_delivery = lowlink_list_delivery.get_text().strip().replace("배송비", "").replace("원", "").replace("포함", "").replace(",", "")
       
            # 최저가 리스트 판매처 명 (이미지 로고인 경우와 text인 경우 발생)
            shop_selector_img = f"#section_price > div.productList_seller_wrap__FZtUS > ul > li:nth-child({i}) > div > div.productList_mall__JtWmC > a > img"
            lowlink_list_shop_img = soup.select_one(shop_selector_img)
            
            shop_selector_text = f"#section_price > div.productList_seller_wrap__FZtUS > ul > li:nth-child({i}) > div > div.productList_mall__JtWmC > a > span"
            lowlink_list_shop_text = soup.select_one(shop_selector_text)
            
            # 이미지로 존재할 경우, 이미지의 대체 텍스트 사용
            if lowlink_list_shop_img:
                lowlinks_shop = lowlink_list_shop_img.attrs['alt']
            elif lowlink_list_shop_text:
                lowlinks_shop = lowlink_list_shop_text.get_text().strip()
            else:
                continue               
            
            data = {
                "productId": productId,
                "link": lowlinks_href,
                "shop": lowlinks_shop,
                "price": lowlinks_price,
                "deliveryfee": lowlinks_delivery
            }
            result.append(data)
        
        driver.quit()
        return result
    
    except Exception as e:
        print(f"Failed to get lowest price link for URL {url}: {e}")
        return None
