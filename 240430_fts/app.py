#!/usr/bin/env python
###
# mongoDB에 입력된 리뷰 받아서 서버에 띄우기 :
# scraping 파일 모듈화하여 수집된 리뷰내용 FastAPI 서버에서 출력가능
# 작성자명 : 장다은
# 작성일자 : 240430
###

from fastapi import FastAPI, HTTPException, Query, Body
from pymongo import MongoClient
from pydantic import BaseModel
import os
import subprocess
from scraping_reviews import collectReviews

app = FastAPI()

client = MongoClient('mongodb://localhost:27017/')
db = client['fts']
reviews_collection = db['reviews']

class Product(BaseModel):
    product_id: str

@app.get('/', status_code=200)
async def hello():
    return {"message": "OK"}

@app.get("/reviews", description="리뷰 결과 조회 API입니다.", status_code=201)
async def get_reviews(product_id: str = Query(None, alias="productId")):
    if product_id is None:
        return {"message": "productId가 입력되지 않았습니다. productId를 입력하세요."}

    # 상품 존재 여부 확인
    product_exists = reviews_collection.count_documents({"productId": product_id})
    if product_exists == 0:
        # 상품이 존재하지 않으면 바로 스크래핑 실행
        scraping_result = collectReviews(product_id)
        if scraping_result:
            return {"message": "Product ID received and scraping code is done", "reviews": scraping_result}
        else:
            return {"message": "스크래핑은 성공했지만 리뷰를 찾을 수 없습니다."}

    # 리뷰 조회
    cursor = reviews_collection.find({"productId": product_id}, {"_id": 0})
    reviews = list(cursor)
    if reviews:
        return reviews  # 리뷰가 있으면 그대로 리스트를 반환합니다.
    else:
        return {"message": "리뷰 검색 결과가 없습니다."}  # 리뷰가 없으면 메시지를 반환합니다.

@app.post("/submit_product")
async def submit_product(product: Product):
    with open("product_id.txt", "w") as file:
        file.write(product.product_id)

    # 스크래핑 실행
    scraping_result = collectReviews(product.product_id)
    if scraping_result:
        return {"message": "Product ID received and executed the scraping script.", "reviews": scraping_result}
    else:
        return {"message": "스크래핑은 성공했지만 리뷰를 찾을 수 없습니다."}