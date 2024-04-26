const express = require('express')
const { Builder, By, until } = require('selenium-webdriver');
const { MongoClient } = require('mongodb');
const cheerio = require('cheerio');
const chromedriver = require('chromedriver');
const app = express()

app.get('/Hello', (req, res)=>{
    async function main() {
        // MongoDB 연결
        const uri = 'mongodb://192.168.1.162:27017/';
        const client = new MongoClient(uri);
        try {
            await client.connect();
            const database = client.db('fts');
            const reviewsCollection = database.collection('reviews');
    
            // Selenium 드라이버 설정
            let driver = await new Builder().forBrowser('chrome').build();
    
            async function collectReviews(product_id, query) {
                const url = `https://search.shopping.naver.com/catalog/${product_id}?query=${query}`;
                try {
                    await driver.get(url);
                    const reviewTabLocator = By.xpath('/html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[1]/ul/li[3]/a');
                    await driver.wait(until.elementLocated(reviewTabLocator), 10000);
    
                    const reviewTab = await driver.findElement(reviewTabLocator);
                    const isSelected = await reviewTab.getAttribute('aria-selected');
    
                    if (isSelected === 'false') {
                        await reviewTab.click();
                        await driver.wait(until.elementIsVisible(driver.findElement(reviewTabLocator)), 10000);
                    }
    
                    await driver.executeScript("window.scrollTo(0, document.body.scrollHeight);");
                    await driver.sleep(2000); // 스크롤 대기 시간
    
                    const pageSource = await driver.getPageSource();
                    const $ = cheerio.load(pageSource);
                    const reviews = $('div.reviewItems_review__DqLYb div.reviewItems_review_text__dq0kE p.reviewItems_text__XrSSf').map((i, el) => $(el).text()).get();
                    for (let i = 0; i < reviews.length; i++) {
                        const document = {
                            productId: product_id,
                            contents: reviews[i],
                            rank: i + 1,
                            date: new Date().toISOString()
                        };
                        await reviewsCollection.insertOne(document);
                    }
                } catch (e) {
                    console.error(`Failed to process URL for product ID ${product_id}: ${e}`);
                }
            }
    
            const product_id_input = 'product123'; // 상품 ID 입력
            const query_input = 'exampleQuery'; // 쿼리 입력
            await collectReviews(product_id_input, query_input);
    
        } finally {
            await driver.quit();
            await client.close();
        }
    }
})

module.exports = app;