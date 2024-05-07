###
# 기능설명 : CRUD를 위한 api 생성
# 작성자명 : 송한나 
# 작성일자 : 2024.05.01
###

from fastapi import FastAPI, status
from typing import Optional
from database import *
from models import *
from lowlink import *
from search_item import *
import requests

app = FastAPI()

# mysql 연결
db = Mysql_conn()
session = db.sessionmaker()

# jsonserver base_url 설정
base_url = 'http://192.168.1.72:5000/items'

# 네이버 openAPI로 검색할 상품의 query 입력받아서 jsonserver에 json파일 업로드 후, 출력
@app.get(
        path='/additemlist', description="검색 후 , jsonserver item 리스트 업로드",
        status_code=status.HTTP_200_OK,
        responses={200:{"description" : "jsonserver 응답"}}
)
async def addItemList(query: Optional[str] = None):
    # client 정보는 get_secret 사용
    client_id = get_secret("client_id")
    client_secret = get_secret("client_secret")
    # get_search_item 함수를 import하여 json파일 생성
    get_search_item(client_id, client_secret, query)
    # jsonserver 재로딩 떄문에 sleep 추가함
    time.sleep(1)
    reponse = requests.get(base_url)
    return reponse.json()

# json server 에 올라간 리스트 불러오기 (기본값)
@app.get(
        path='/itemlist', description="jsonserver item 리스트",
        status_code=status.HTTP_200_OK,
        responses={200:{"description" : "jsonserver 응답"}}
)
async def getItemList():
    response = requests.get(base_url)
    data = response.json()
    return data

# json server 에 올라간 리스트 불러오기 (최저가)
@app.get(
        path='/sortitemlist', description="jsonserver item 리스트",
        status_code=status.HTTP_200_OK,
        responses={200:{"description" : "jsonserver 응답"}}
)
async def getItemList():
    response = requests.get(base_url)
    data = response.json()
    # 함수를 사용하여 lprice 최저가순 정렬
    sorted_data = sorted(data, key=lambda x: int(x['lprice']))
    return sorted_data


# productId값 입력 받아서 해당 productId와 동일한 값을 mysql 저장 (중복 값 확인하고, 존재하면 mysql 에서 꺼내오기 )
@app.post(
    path='/additem/{productId}', description="jsonserver item 선택해서 mysql 저장",
    status_code=status.HTTP_200_OK,
    responses={200:{"description" : "mysql 저장 완료"}}
)
async def addItem(productId: Optional[str] = None):
    if productId is None:
        return "productId를 입력하세요."
    else:
        # 받아온 productId 로 중복값 먼저 확인
        checkId = session.query(Item).filter(Item.productId == productId).first()
        # 만약 mysql에 없으면 새로 저장
        if checkId is None:
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
            # item table 저장
            item = Item(productId=selected_data['productId'], title=selected_data['title'], link=selected_data['link'], image=selected_data['image'], lprice=selected_data['lprice'])
            session.add(item)
            session.commit()
            # #lowlink table 저장
            link = Lowlink(productId=selected_data['productId'])
            session.add(link)
            session.commit()
            # mysql table 해당 값 조회
            itemresult = session.query(Item).filter(Item.productId == productId).first()
            return {"result code": 200, "item": itemresult}
        else:
            return {"result code": 200, "item": checkId}
        
    
# 담은 item table 전체 조회 (최근 본 상품)
@app.get(
        path='/getitems', description="mysql item table 전체 조회",
        status_code=status.HTTP_200_OK,
        responses={200:{"description" : "mysql 조회 완료"}}
)
async def getItems():
    result = session.query(Item).all()
    return {"result code": 200,"item":result}

# 담은 item table 중 선택해서 출력 (확인용)
@app.get(
        path='/getitem/{productId}',description="mysql item table 선택 조회",
        status_code=status.HTTP_200_OK,
        responses={200:{"description" : "mysql 선택 조회 완료"}}
)
async def getItem(productId: Optional[str] = None):
    if productId is None:
        return "productId를 입력하세요."
    else:
        result = session.query(Item).filter(Item.productId == productId).first()
        return {"result code": 200,"item":result}

# 최근 본 상품에서 삭제 했을 때, productId값으로 mysql, mongodb에서 삭제
@app.post(
        path='/deleteitem/{productId}',description="mysql item table 선택 삭제",
        status_code=status.HTTP_200_OK,
        responses={200:{"description" : "mysql 선택 삭제 완료"}}
)
async def deleteItem(productId: Optional[str] = None):
    if productId is None:
        return "productId를 입력해주세요"
    else:
        # mysql - item table delete
        session.query(Item).filter(Item.productId == productId).delete()
        session.commit()
        # mysql - lowlink table delete
        session.query(Lowlink).filter(Lowlink.productId == productId).delete()
        session.commit()
        # mongodb delete
        mycol.delete_many({"productId":productId})

        result = session.query(Item).all()
        return {"result code": 200,"item":result}

# 상품 선택했을 때, 크롤링 한 정보를 몽고에 저장 (중복 확인하고 존재하면 몽고 에서 꺼내오기 )
@app.post(
    path='/addlowlink/{productId}',
    description="상품 최저가 정보 mongoDB에 저장",
    status_code=status.HTTP_200_OK,
    responses={200:{"description" : "mongoDB 저장 완료"}}
)
async def addLowLink(productId: Optional[str] = None):
    if productId is None:
        return "productId를 입력하세요."
    else:
        # MongoDB에서 해당 제품의 정보 조회
        existing_item = list(mycol.find({"productId":productId}, {"_id":0}))
        # MongoDB에 해당 제품의 정보가 없으면 새로운 데이터 저장
        if not existing_item:
            url = f"https://search.shopping.naver.com/catalog/{productId}?&section=price"
            lowitem = get_lowest_price(url, productId)
            mycol.insert_many(lowitem)
            time.sleep(3)
            result = list(mycol.find({"productId": productId}, {"_id": 0}))
            return {"result code": 200,"lowlinklist": result}
        # MongoDB에 해당 제품의 정보가 있으면 저장된 정보 반환
        else:
            return {"result code": 200,"lowlinklist": existing_item}

# 몽고 디비 전체 조회 (확인용)
@app.get(
    path='/getlowlink/{productId}',description="상품 최저가 정보 mongoDB 조회",
    status_code=status.HTTP_200_OK,
    responses={200:{"description" : "mongoDB 조회 완료"}}
)
async def getLowlink(productId: Optional[str] = None):
    result = list(mycol.find({"productId":productId}, {"_id":0}))
    return {"result code": 200,"lowlinklist":result}


