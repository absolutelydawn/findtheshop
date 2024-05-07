///
// fastAPI 데이터 node서버에 출력하고 html파일과 연결하기 : 
// productId를 전달받으면 post > get 동작 연결하여 수집/조회 결과 출력
// reviews.html과 연결하여 프론트 페이지 동작 확인 완료 (front server 추가해야됨!)
// url : productId query > params로 받음 /reviews/{productId}
// 작성자명 : 장다은
// 작성일자 : 240501
///

const express = require('express');
const axios = require('axios');
const router = express.Router();

// 환경변수를 사용하여 API 서버 URL 설정
const apiUrl = process.env.API_SERVER || 'http://localhost:3500';

// 리뷰 데이터 API 라우팅
router.get('/reviews/:productId', (req, res) => {
    const productId = req.params.productId;

    axios.get(`${apiUrl}/reviews/${productId}`)
        .then(reviewResponse => {
            res.json(reviewResponse.data);
        })
        .catch(reviewError => {
            console.error(reviewError.response ? reviewError.response.data : reviewError.message);
            res.status(500).json({ message: 'Error fetching reviews', error: reviewError.message });
        });
});

module.exports = router; // 라우터 모듈로 내보내기