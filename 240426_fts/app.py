#!/usr/bin/env python
###
# mongoDB에 입력된 리뷰 받아서 서버에 띄우기 :
# mongoDB에 수집된 리뷰내용  FastAPI서버에서 출력하기
# myscript.sh로 스크래핑 파일 실행 > mongoDB에 담은 뒤 리뷰내용 조회가능ㄴ
# 작성자명 : 장다은
# 작성일자 : 240426
# 기타사항 : 
# 개선 ) 리뷰내용 조회 시 개선사항 _ productId 있는데 리뷰 없는 경우 / productId가 잘못된 경우 고려
#        리뷰내용 파싱 추가 : rank(별점), date(작성일자)   
###
from fastapi import FastAPI, HTTPException, Query, Body
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId
import os
import subprocess

app = FastAPI()

client = MongoClient('mongodb://localhost:27017/')
db = client['fts']
reviews_collection = db['reviews']

class Product(BaseModel):
    product_id: str

# main page(추후수정)
@app.get('/', status_code=200)
async def hello():
    return "OK"

# productId를 검색하여 리뷰 내용 출력
# (추후 개선하기) productId는 있는데 리뷰가 없는 경우 / productId가 잘못된 경우 고려하기
@app.get("/reviews", description="리뷰 결과 조회 API입니다.", status_code=201)
async def getReviews(product_id: str = Query(None, alias="productId")):
    # productId가 입력되지 않은 경우
    if product_id is None:
        return {"message": "productId가 입력되지 않았습니다. productId를 입력하세요."}
    
    # MongoDB에서 productId에 해당하는 리뷰 찾기
    cursor = reviews_collection.find({"productId": product_id}, {"_id": 0})
    reviews = list(cursor)
    if reviews:
        return reviews
    else: # 리뷰가 없다면
        return {"message": "리뷰 검색 결과가 없습니다."}
    
# selenium파일에 인자값(productId) 전달하기
@app.post("/submit_product")
async def submit_product(product: Product):
    with open("product_id.txt", "w") as file:
        file.write(product.product_id)
    
    subprocess.run(["./myscript.sh"], check=True)
    return {"message": "Product ID received and executed the scraping script."}
