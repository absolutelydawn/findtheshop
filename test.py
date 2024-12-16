from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def get_lowest_price_link(url):
    try:
        display = Display(visible=0, size=(1920, 1080))
        display.start()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        lowest_price_links = []
        for i in range(1, 4):
            # 최저가 링크
            lowest_price_link = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, f'//*[@id="section_price"]/div[4]/ul/li[{i}]/div/div[2]/a'))
            ).get_attribute('href')
            lowest_price_links.append(lowest_price_link)
        driver.quit()
        return lowest_price_links
    except Exception as e:
        print(f"Failed to get lowest price link for URL {url}: {e}")
        return None
    
# 최저가 item의 상품판매처
def get_lowest_price_shop(url):
    try:
        display = Display(visible=0, size=(1920, 1080))
        display.start()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        lowest_price_shops = []
        for i in range(1, 4):
            # 최저가 샵 명
            lowest_price_shop = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, f'//*[@id="section_price"]/div[4]/ul/li[{i}]/div/div[1]/a/img'))
            ).get_attribute('alt')
            lowest_price_shops.append(lowest_price_shop)
        driver.quit()
        return lowest_price_shops
    except Exception as e:
        print(f"Failed to get lowest price shop : {e}")
        return None
    
# 최저가 item의 가격
def get_lowest_price(url):
    try:
        display = Display(visible=0, size=(1920, 1080))
        display.start()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        lowest_prices = []
        for i in range(1, 4):
            # 현재 최저가격
            lowest_price = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, f'//*[@id="section_price"]/div[4]/ul/li[{i}]/div/div[3]/a/span/em'))
            ).text
            lowest_prices.append(lowest_price)  
        driver.quit()        
        return lowest_prices
    except Exception as e:
        print(f"Failed to get lowest price : {e}")
        return None
    
# 최저가 item의 배송비 
def get_lowest_price_delivery(url):
    try:
        display = Display(visible=0, size=(1920, 1080))
        display.start()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        lowest_deliverys = []
        for i in range(1, 4):
            # 현재 배송비
            lowest_delivery = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, f'//*[@id="section_price"]/div[4]/ul/li[1]/div/div[3]/div[1]/div/text()'))
            )
            lowest_deliverys.append(lowest_delivery)
        driver.quit()      
        return lowest_deliverys
    except Exception as e:
        print(f"Failed to get lowest deliverys : {e}")
        return None