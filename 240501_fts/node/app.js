///
// fastAPI 데이터 node서버에 출력하고 html파일과 연결하기 : 
// productId를 전달받으면 post > get 동작 연결하여 수집/조회 결과 출력
// reviews.html과 연결하여 프론트 페이지 동작 확인 완료 (front server 추가해야됨!)
// url : productId query > params로 받음 /reviews/{productId}
// 작성자명 : 장다은
// 작성일자 : 240501
///

const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '../config/.env') });// 환경 변수를 로드하기 위해 추가
const axios = require('axios');
const express = require('express');
const cors = require('cors');

const app = express();

// 정적 파일 제공 설정
app.use(express.static(path.join(__dirname, '../scripts')));

app.use(cors({
    origin: '*', // 모든 출처 허용 옵션
}))

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../scripts', 'reviews.html')); // HTML 페이지 제공
});

app.get('/reviews/:productId', (req, res) => {
    const productId = req.params.productId;
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
