#!/usr/bin/env python
###
# mongoDB에 입력된 리뷰 받아서 서버에 띄우기 :
# scraping 파일 모듈화하여 수집된 리뷰내용 FastAPI 서버에서 출력가능
# 리뷰내용들 {"reviews" : reviews} 로 반환(json)
# GET으로 받으면 mongoDB검토 후 스크래핑로직 실행하기때문에 POST 삭제
# GET method 경로 수정함
# MySQL 연결 완료
# 작성자명 : 장다은
# 작성일자 : 240430
###

from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from database import SessionLocal  # database 모듈에서 SessionLocal 임포트
from models import ProductID  # models 모듈에서 ProductID 모델 임포트
from scraping_reviews import collectReviews
from bson import ObjectId  # ObjectId 처리를 위해 bson 모듈 추가
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# 상대 경로 사용하여 .env 파일 로드
load_dotenv("../config/.env")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# MongoDB 설정
client = MongoClient('mongodb://localhost:27017/')
db = client['fts']
reviews_collection = db['reviews']

class Product(BaseModel):
    product_id: str

@app.get('/')
async def hello():
    return {"message": "OK"}

def transform_id(document):
    if '_id' in document:
        document['_id'] = str(document['_id'])  # ObjectId를 문자열로 변환
    return document

@app.get("/reviews/{productId}", status_code=200)
async def get_reviews(productId: Optional[str] = None):
    if productId is None:
        raise HTTPException(status_code=400, detail="productId가 입력되지 않았습니다. productId를 입력하세요.")

    # MySQL에서 상품 존재 여부 확인
    with SessionLocal() as session:
        product_exists_in_mysql = session.query(ProductID).filter(ProductID.product_id == productId).first()
    
    # MongoDB에서 리뷰 존재 여부 확인
    product_exists_in_mongo = reviews_collection.count_documents({"productId": productId}) > 0

    if not product_exists_in_mysql and not product_exists_in_mongo:
        # 상품이 MySQL과 MongoDB에 모두 존재하지 않으면 스크래핑 실행
        scraping_result = collectReviews(productId)
        if scraping_result:
            # 스크래핑 결과가 있으면 MySQL에 상품 ID 저장
            with SessionLocal() as session:
                session.add(ProductID(product_id=productId))
                session.commit()
            # MongoDB에 리뷰 데이터 저장
            return {"message": "Product ID received and scraping code is done", "reviews": [transform_id(review) for review in scraping_result]}
        else:
            return {"message": "스크래핑은 성공했지만 리뷰를 찾을 수 없습니다."}

    # MySQL이나 MongoDB에 상품이 존재하면 MongoDB에서 리뷰 조회
    if product_exists_in_mongo:
        cursor = reviews_collection.find({"productId": productId}, {"_id": False})
        reviews = [transform_id(review) for review in list(cursor)]
        if reviews:
            return {"reviews": reviews}
        else:
            return {"message": "리뷰 검색 결과가 없습니다."}
    else:
        return {"message": "리뷰 검색 결과가 없습니다."}
    
# @app.delete() >> delete 로직 완성하기
