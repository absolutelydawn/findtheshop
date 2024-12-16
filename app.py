from fastapi import FastAPI, status
from typing import Optional
from pymongo import mongo_client
from database import Mysql_conn
from models import *
from lowlink import *
from search_item import *
import requests
import os.path
import json

app = FastAPI()

db = Mysql_conn()
session = db.sessionmaker()

#mongodb 연결
BASE_DIR = os.path.dirname(os.path.relpath("./"))
secret_file = os.path.join(BASE_DIR, 'secret.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        errorMsg = "Set the {} environment variable.".format(setting)
        return errorMsg
 
# jsonserver - itemlist (정제 필요함)
base_url = 'http://0.0.0.0:5000/items'
@app.get(
        path='/itemlist', description="jsonserver item 리스트",
        status_code=status.HTTP_200_OK,
        responses={200:{"description" : "jsonserver 응답"}}
)
async def getItemList():
    reponse = requests.get(base_url)
    return reponse.json()

# item 입력받아서 jsonserver에 업로드
@app.post(
        path='/additemlist', description="검색 후 , jsonserver item 리스트 업로드",
        status_code=status.HTTP_200_OK,
        responses={200:{"description" : "jsonserver 응답"}}
)
# client_id, client_secret
async def addItemList(query: Optional[str] = None):
    client_id = get_secret("client_id")
    client_secret = get_secret("client_secret")
    get_search_item(client_id, client_secret, query)
    time.sleep(2)
    reponse = requests.get(base_url)
    return reponse.json()

# item 선택해서 mysql 저장
@app.post(
        path='/additem/{productId}', description="jsonserver item 선택해서 mysql 저장",
        status_code=status.HTTP_200_OK,
        responses={200:{"description" : "mysql 저장 완료"}}
)
async def addItem(productId: Optional[str] = None):
    if productId is None:
        return "productId를 입력하세요."
    else:
        url = base_url + '?' + 'productId=' + productId
        response = requests.get(url)
        product_data = response.json()  
        selected_data = {
            'title': product_data[0]['title'],
            'link': product_data[0]['link'],
            'image': product_data[0]['image'],
            'lprice': product_data[0]['lprice'],
            'productId': product_data[0]['productId']
        }
        item = Itemtest(title=selected_data['title'],link=selected_data['link'],image=selected_data['image'],lprice=selected_data['lprice'],productId=selected_data['productId'])
        session.add(item)
        session.commit()
        result = session.query(Itemtest).filter(Itemtest.productId == productId).first()
        return result
    
# 담은 item table 전체 조회
@app.get(
        path='/getitems', description="mysql item table 전체 조회",
        status_code=status.HTTP_200_OK,
        responses={200:{"description" : "mysql 조회 완료"}}
)
async def getItems():
    result = session.query(Itemtest)
    return result.all()

# 담은 item table 중 선택해서 출력
@app.get(
        path='/getitem/{productId}',description="mysql item table 선택 조회",
        status_code=status.HTTP_200_OK,
        responses={200:{"description" : "mysql 선택 조회 완료"}}
)
async def getItem(productId: Optional[str] = None):
    if productId is None:
        return "productId를 입력하세요."
    else:
        result = session.query(Itemtest).filter(Itemtest.productId == productId).first()
        return result

# item table에서 삭제할 productId 입력  후, 삭제
@app.get(
        path='/deleteitem/{productId}',description="mysql item table 선택 삭제",
        status_code=status.HTTP_200_OK,
        responses={200:{"description" : "mysql 선택 삭제 완료"}}
)
async def deleteItem(productId: Optional[str] = None):
    if productId is None:
        return "productId를 입력해주세요"
    else:
        session.query(Itemtest).filter(Itemtest.productId == productId).delete()
        session.commit()
        result = session.query(Itemtest).all()
        return result

# mongodb 접속
MONGOHOSTNAME = get_secret("Local_Mongo_Hostname")
MONGOUSERNAME = get_secret("Local_Mongo_Username")
MONGOPASSWORD = get_secret("Local_Mongo_Password")

client = mongo_client.MongoClient(f'mongodb://{MONGOUSERNAME}:{MONGOPASSWORD}@{MONGOHOSTNAME}')
mydb = client['findtheshop']
mycol = mydb['lowlink']

# 상품 선택했을 때, productid와 title받아서 셀레니움으로 크롤링 가동하고 > 긁어온 링크를 몽고에 저장 > 그걸또 바로보여줌 가능??? 응가능
# mongodb에 먼저 확인하는 작업 필요함
@app.post('/addlowlink/{productId}')
async def addLowLink(productId: Optional[str] = None):
    url=f"https://search.shopping.naver.com/catalog/{productId}?&section=price"
    lowitem = get_lowest_price(url, productId)
    mycol.insert_many(lowitem)
    data = list(mycol.find({}, {"_id":0}).limit(100))
    # mysql에 productId만 insert (나중에 select, drop을 위해)
    item = Lowlink(productID=productId)
    session.add(item)
    session.commit()
    return(data)

# 몽고에 담은 내용  확인하기
@app.get('/getlowlink/{productId}')
async def getLowlink(productId: Optional[str] = None):
    result = list(mycol.find({"productId":productId}, {"_id":0}))
    return(result)
