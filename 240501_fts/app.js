///
// fastAPI 데이터 node서버에 출력하고 html파일과 연결하기 : 
// productId를 전달받으면 post > get 동작 연결하여 수집/조회 결과 출력
// reviews.html과 연결하여 프론트 페이지 동작 확인 완료 (front server 추가해야됨!)
// 작성자명 : 장다은
// 작성일자 : 240501
///

require('dotenv').config(); // 환경 변수를 로드하기 위해 추가
const axios = require('axios');
const express = require('express');
const path = require('path');

const app = express();

app.use(express.static(path.join(__dirname, 'public'))); // 정적 파일 제공 설정

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'reviews.html')); // HTML 페이지 제공
});

app.get('/submit-and-fetch-reviews', (req, res) => {
    const productId = req.query.productId;
    const apiUrl = process.env.API_SERVER || 'http://localhost:3500'; // 환경 변수 사용

    axios.get(`${apiUrl}/reviews/${productId}`)
        .then(reviewResponse => {
            res.json(reviewResponse.data);
        })
        .catch(reviewError => {
            console.error(reviewError.response ? reviewError.response.data : reviewError.message);
            res.status(500).json({ message: 'Error fetching reviews', error: reviewError.message });
        });
});

app.listen(3000, () => console.log('Server running on http://localhost:3000'));
