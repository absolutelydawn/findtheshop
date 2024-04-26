#!/bin/bash

# product_id.txt 파일로부터 product_id 읽기
PRODUCT_ID=$(cat product_id.txt)

# scraping_reviews.py 스크립트 실행
python scraping_reviews.py $PRODUCT_ID

# 실행 결과에 따른 처리
if [ $? -eq 0 ]; then
    echo "Scraping script executed successfully."
else
    echo "Failed to execute scraping script."
fi