from selenium import webdriver
from pyvirtualdisplay import Display 
import time
from bs4 import BeautifulSoup


def get_lowest_price(url, productId):
    try: 
        # for Linux : Linux 환경에서 selenium 실행 시 필요한 옵션
        display = Display(visible=0, size=(1920, 1080))
        display.start()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        output = []
        for i in range(1, 4):
            # 최저가 리스트 링크
            link_selector = f"#section_price > div.productList_seller_wrap__FZtUS > ul  li:nth-child({i}) > div > div.productList_price__2eGt4 > a"
            lowlink_list_link = soup.select_one(link_selector)
            # 최저가 리스트 가격
            price_selector = f"#section_price > div.productList_seller_wrap__FZtUS > ul > li:nth-child({i}) > div > div.productList_price__2eGt4 > a > span > em"
            lowlink_list_price = soup.select_one(price_selector)
            # 최저가 리스트 배송비
            delivery_selector = f"#section_price > div.productList_seller_wrap__FZtUS > ul > li:nth-child({i}) > div > div.productList_price__2eGt4 > div.productList_delivery__WwSwL"
            lowlink_list_delivery = soup.select_one(delivery_selector)

            if lowlink_list_link:
                lowlinks_href = lowlink_list_link.attrs['href']
                lowlinks_price = lowlink_list_price.get_text().strip().replace(",", "")
                lowlinks_delivery = lowlink_list_delivery.get_text().strip().replace("배송비", "").replace("원", "").replace("포함", "").replace(",", "")
       
                # 최저가 리스트 판매처 이름
                shop_selector_img = f"#section_price > div.productList_seller_wrap__FZtUS > ul > li:nth-child({i}) > div > div.productList_mall__JtWmC > a > img"
                lowlink_list_shop_img = soup.select_one(shop_selector_img)
                
                shop_selector_text = f"#section_price > div.productList_seller_wrap__FZtUS > ul > li:nth-child({i}) > div > div.productList_mall__JtWmC > a > span"
                lowlink_list_shop_text = soup.select_one(shop_selector_text)
                
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
                output.append(data)
        
        driver.quit()
        return output
    
    except Exception as e:
        print(f"Failed to get lowest price link for URL {url}: {e}")
        return None
