///
// fastAPI 데이터 node서버에 출력하기 : 
// productId를 전달받으면 post > get 동작 연결하여 수집/조회 결과 출력
// 작성자명 : 장다은
// 작성일자 : 240430
///

const axios = require('axios');
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));

// [GET] 홈페이지
app.get('/', (req, res) => {
  res.send('<form method="post" action="/submit-and-fetch-reviews">Product ID: <input type="text" name="productId"/><input type="submit" value="Submit"/></form>');
});

// [POST] Node.js >> FastAPI 요청 >> [GET] 요청결과 바로 받아오기 
app.post('/submit-and-fetch-reviews', (req, res) => {
    const productId = req.body.productId;
    axios.get(`http://localhost:3500/reviews?productId=${productId}`)
    .then(reviewResponse => {
        res.send(reviewResponse.data);
    }).catch(reviewError => {
        console.error(reviewError.response ? reviewError.response.data : reviewError.message);
        res.send('Error fetching reviews: ' + reviewError.message);
    });
});

// 서버를 포트 3000에서 실행
app.listen(3000, () => console.log('Server running on http://localhost:3000'));
