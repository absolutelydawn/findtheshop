from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# for Linux : Linux 환경에서 selenium 실행 시 필요한 옵션
display = Display(visible=0, size=(1920, 1080))
display.start()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=chrome_options)
###  

def get_lowest_price_link(url):
    try:
        driver.get(url)
        # 최저가 링크 3개와 샵 명, 현재 최저가격 가져오기
        lowest_price_links = []
        lowest_price_shops = []
        lowest_prices = []
        #lowest_deliverys = []

        for i in range(1, 4):
            # 최저가 링크
            lowest_price_link = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, f'//*[@id="section_price"]/div[4]/ul/li[{i}]/div/div[2]/a'))
            ).get_attribute('href')
            lowest_price_links.append(lowest_price_link)

            # # 최저가 샵 명
            # lowest_price_shop = WebDriverWait(driver, 10).until(
            #     EC.visibility_of_element_located((By.XPATH, f'//*[@id="section_price"]/div[4]/ul/li[{i}]/div/div[1]/a/img'))
            # ).get_attribute('alt')
            # lowest_price_shops.append(lowest_price_shop)

            # # 현재 최저가격
            # lowest_price = WebDriverWait(driver, 10).until(
            #     EC.visibility_of_element_located((By.XPATH, f'//*[@id="section_price"]/div[4]/ul/li[{i}]/div/div[3]/a/span/em'))
            # ).text
            # lowest_prices.append(lowest_price)

            # # 현재 배송비
            # lowest_delivery = WebDriverWait(driver, 10).until(
            #     EC.visibility_of_element_located((By.XPATH, f'//*[@id="section_price"]/div[4]/ul/li[1]/div/div[3]/div[1]/div/text()'))
            # )
            # lowest_deliverys.append(lowest_delivery)

        return lowest_price_links, lowest_price_shops, lowest_prices


    except Exception as e:
        print(f"Failed to get lowest price link for URL {url}: {e}")
        return None
    
if __name__ == "__main__":
    get_lowest_price_link()