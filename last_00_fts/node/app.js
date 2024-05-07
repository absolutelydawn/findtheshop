const express = require('express');
const morgan = require('morgan');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '../config/.env') });
const cors = require('cors');

const app = express();
app.set('port', process.env.PORT || 8500);

app.use(morgan('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(cors({ origin: '*' })); // 모든 접근 허용
app.use(express.static(path.join(__dirname, '../public'))); // 정적 파일 경로 수정

// main 라우터 임포트 및 사용
const mainRouter = require('./main');
app.use('/', mainRouter);

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../public', 'reviews.html')); // HTML 페이지 제공
});

// 서버 시작
app.listen(app.get('port'), () => {
    console.log(`${app.get('port')} Port: Server started~!!`);
});
