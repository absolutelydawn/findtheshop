const axios = require('axios');
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));

// 홈페이지 GET
app.get('/', (req, res) => {
  res.send('<form method="post" action="/submit-and-fetch-reviews">Product ID: <input type="text" name="productId"/><input type="submit" value="Submit"/></form>');
});

// 사용자 입력을 FastAPI 서버로 전송하는 POST 요청
app.post('/submit-and-fetch-reviews', (req, res) => {
    const productId = req.body.productId;
    axios.post('http://localhost:3500/submit_product', {
        product_id: productId
    }, {
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => {
        // POST 요청 성공 후, 바로 GET 요청을 실행
        axios.get('http://localhost:3500/reviews', {
            params: { productId: productId }
        }).then(reviewResponse => {
            res.send(reviewResponse.data);
        }).catch(reviewError => {
            res.send('Error fetching reviews after submission: ' + reviewError.message);
        });
    }).catch(submitError => {
        console.error(submitError.response ? submitError.response.data : submitError.message);
        res.send('Error submitting product: ' + submitError.message);
    });
});

// 서버를 포트 3000에서 실행
app.listen(3000, () => console.log('Server running on http://localhost:3000'));
