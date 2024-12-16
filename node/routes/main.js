const express = require('express')
const bodyParser = require('body-parser')
const XMLHttpRequest = require("xhr2");

const app = express()

app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

// 검색 후 , 쿼리 받아서 리스트 띄우기
app.post('/itemlist', async (req, res) => {
    try {
        const xhr = new XMLHttpRequest();
        const encodedQuery = encodeURIComponent(req.body.query);
        const url = `http://192.168.1.72:3000/additemlist?query=${encodedQuery}`;
        xhr.open("POST", url);
        xhr.setRequestHeader("content-type", "application/json; charset=UTF-8");
        const data = { query: req.body.query};
        xhr.send(JSON.stringify(data));
        xhr.onload = () => {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.response);
                setTimeout(() => {
                    let output = '<link rel="stylesheet" href="/itemlist.css"><link rel="stylesheet" href="/reset.css">';
                    response.forEach((item, index) => {
                        output += `<h1>${index}: ${item.title}</h1>`;
                        output += `<a href="/iteminfo?productId=${item.productId}"><img src="${item.image}" alt="Product Image"></a>`;
                        output += `<p>Price: ${item.lprice}</p>`;
                        output += '<hr>';
                    });
                    res.send(output);
                }, 3000); 
            } else {
                console.log(xhr.status, xhr.statusText);
                res.status(500).send('Internal Server Error');
            }
        };
    } catch (error) {
        console.error(error);
        res.status(500).send('Internal Server Error');
    }
});

app.get('/iteminfo', async (req, res) => {
    try {
        const productId = req.query.productId;
        const data = { productId: productId }; 
        // 상품 정보 mysql 추가
        const addItemResponse = await fetch(`http://192.168.1.72:3000/additem/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        if (!addItemResponse.ok) {
            throw new Error('Failed to add low link data to the database');
        }
        // 상품 최저가 정보 mongodb에 추가
        const addLowLinkResponse = await fetch(`http://192.168.1.72:3000/addlowlink/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        if (!addLowLinkResponse.ok) {
            throw new Error('Failed to add low link data to the database');
        }
        // 상품 정보와 최저가 정보를 병렬로 가져옴
        const [itemResponse, linkResponse] = await Promise.all([
            fetch(`http://192.168.1.72:3000/getitem/${productId}`).then(response => response.json()),
            fetch(`http://192.168.1.72:3000/getlowlink/${productId}`).then(response => response.json())
        ]);

        // 클라이언트에게 응답
        let output = '<link rel="stylesheet" href="/itemlist.css"><link rel="stylesheet" href="/reset.css">';

        // 상품 정보 추가
        output += `<h1>${itemResponse.title}</h1>`;
        output += `<img src="${itemResponse.image}" alt="Product Image">`;

        // 최저가 정보 추가
        linkResponse.forEach((item) => {
            output += `<a href="${item.link}" target="_blank">최저가 링크</a>`; 
            output += `<p>판매처: ${item.shop || "N/A"}</p>`;
            output += `<p>최저가: ${item.price || "N/A"}</p>`;
            output += '<hr>';
        });

        res.send(output);
    } catch (error) {
        console.error(error);
        res.status(500).send('Internal Server Error');
    }
});




module.exports = app;