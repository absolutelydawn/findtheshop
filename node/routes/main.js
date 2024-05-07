const express = require('express')
const bodyParser = require('body-parser')

const app = express()

app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

// 메인 화면 - 최근 본 상품 
app.get('/view', async (req, res) => {
    try {
        const response = await fetch('http://192.168.1.72:3000/getitems');
        const data = await response.json();
        const recentItems = data.item

        // 메인 화면에 최신 순 4개 출력을 위한 sort 사용
        const sortedItems = recentItems.sort((a, b) => b.id - a.id).slice(0, 4);
        let output = '<link rel="stylesheet" href="/main.css"><link rel="stylesheet" href="/reset.css">';
        output += `
                <h2 style="margin:30px 0">최근 본 상품</h2>
                    <ul class="item-list">
        `;

        sortedItems.forEach((item) => {
            output += `
                <li class="item">
                    <a href="/iteminfo?productId=${item.productId}" target="_blank">
                        <img src="${item.image}" alt="${item.title}">
                    </a>
                    <h4>${item.title}</h4>
                    <p>현재 최저가 <strong style="color:#f56565">${item.lprice}</strong> 원</p>
                </li>
            `;
        });
        output += `
                    </ul>
        `;
        res.send(output);
    } catch (error) {
        console.error(error);
        res.status(500).send('Internal Server Error');
    }
});

// 최근 본 상품 전체 목록 페이지
app.get('/views', async (req, res) => { 
    try {
        const response = await fetch('http://192.168.1.72:3000/getitems');
        const data = await response.json();
        const recentItems = data.item
        let output = `  
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <meta charset="UTF-8">
                            <title>FINDTHESHOP-최근 본 상품</title>
                            <link rel="stylesheet" href="/main.css">
                            <link rel="stylesheet" href="/reset.css">
                        </head>
                        <body>
                        <div id="wrap">
                            <nav>
                                <div class="logo"><a href="/">#FINDTHESHOP</a></div>
                                <div class="navbar">
                                    <ul>
                                        <li><a href="/">HOME</a></li>
                                        <li><a href="views" target="_self">Product</a></li>
                                    </ul>
                                </div>
                            </nav>
                            <h2 style="text-align:center; margin:30px 0">최근 본 상품 전체 리스트</h2>
                        </div>
                        <div id="wrap">
                        <ul class="item-list">
                    `;
        recentItems.forEach((item) => {
            output += `
                <li class="item">
                    <a href="/iteminfo?productId=${item.productId}" target="_blank">
                        <img src="${item.image}" alt="Product Image">
                    </a>
                    <h4>${item.title}</h4>
                    <p>현재 최저가 <strong style="color:#f56565">${item.lprice}</strong> 원</p>
                    <div class="delete-btn" data-product-id="${item.productId}">삭제</div>
                </li>
            `;
        });
        output += `
                </ul>
                </div>
                <script>
                // 삭제 버튼 클릭 시 - 상품 삭제 후, reload
                document.querySelectorAll('.delete-btn').forEach(btn => {
                    btn.addEventListener('click', async () => {
                        const productId = btn.dataset.productId;
                        const confirmation = confirm('해당 상품을 삭제하시겠습니까?');
                        // 화면 reload
                        window.location.reload();
                        if (confirmation) {
                            try {
                                const response = await fetch('http://192.168.1.72:3000/deleteitem/' + productId, {
                                    method: 'POST'
                                });
                                const data = await response.json();
                                const recentItems = data.item 
                            } catch (error) {
                                console.error(error);
                            }
                        }
                    });
                });
                </script>
            </body>
            </html>
        `;
        res.send(output);
    } catch (error) {
        console.error(error);
        res.status(500).send('Internal Server Error');
    }
});

// 검색 후 , 쿼리 받아서 리스트 띄우기 (처음 검색 시 - 쿼리 받아서 출력해야해서 페이지 따로 생성함)
app.get('/itemlist', async (req, res) => {
    try {
        const encodedQuery = encodeURIComponent(req.query.query);
        const additemResponse = await fetch(`http://192.168.1.72:3000/additemlist?query=${encodedQuery}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const addItemData = await additemResponse.json();
        let output = `  
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <meta charset="UTF-8">
                            <title>FINDTHESHOP-상품 조회 결과</title>
                            <link rel="stylesheet" href="/main.css">
                            <link rel="stylesheet" href="/reset.css">
                        </head>
                        <body>
                        <button onclick="topFunction()" id="topBtn" title="Go to top">TOP</button>
                        <div id="wrap">
                            <nav>
                                <div class="logo"><a href="/">#FINDTHESHOP</a></div>
                                <div class="navbar">
                                    <ul>
                                        <li><a href="/">HOME</a></li>
                                        <li><a href="views" target="_self">Product</a></li>
                                    </ul>
                                </div>
                            </nav>
                            <h2 style="text-align:center; margin:30px 0"> " ${req.query.query} " 검색 결과입니다</h2>
                            <ul class="Btn">
                                <li class="btn-click"><a href="deitemlist?query=${req.query.query}" target="_self">기본순</a></li>
                                <li class="lowbtn"><a href="sortitemlist?query=${req.query.query}" target="_self">최저가순</a></li>
                            </ul>
                        </div>
                        <div id="wrap">
                        <ul class="item-list">
                    `;
                    addItemData.forEach((item) => { 
                        output += `
                            <li class="item">
                                <a href="/iteminfo?productId=${item.productId}" target="_self">
                                    <img src="${item.image}" alt="Product Image">
                                </a>
                                <h4>${item.title}</h4>
                                <p>현재 최저가 <strong style="color:#f56565">${item.lprice}</strong> 원</p>
                            </li>
                        `;
                    });
                    output += `
                                </ul>
                                </div>
                                <script>
                    `;
                    output += `
                                    function sortByDefault() {
                                        window.location.reload();
                                    }
                                    // window 스크롤 이벤트 사용
                                    window.onscroll = function() {scrollFunction()};

                                    function scrollFunction() {
                                    // 스크롤이 20px 이상 내려갔을 때 top 버튼 생성
                                    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
                                        document.getElementById("topBtn").style.display = "block";
                                    } else {
                                        document.getElementById("topBtn").style.display = "none";
                                    }
                                    }

                                    // TOP 버튼을 클릭시 페이지의 맨 위로 이동
                                    function topFunction() {
                                    document.body.scrollTop = 0; // Safari
                                    document.documentElement.scrollTop = 0; // Chrome, Firefox, IE 및 Opera
                                    }

                    `;
                    output += `
                                </script>
                                </body>
                                </html>
                    `;
                    res.send(output);
    }
    catch{
        res.status(500).send('Internal Server Error');
    }
});

// 최저가 순 에서 기본 순으로 이동 시, query 가 없으므로 다시 itemlist 출력하는 페이지 생성
app.get('/deitemlist', async (req, res) => { // req 매개변수 추가
    try {
        const response = await fetch('http://192.168.1.72:3000/itemlist');
        const data = await response.json();
        let output = `  
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <meta charset="UTF-8">
                            <title>FINDTHESHOP-상품 조회 결과</title>
                            <link rel="stylesheet" href="/main.css">
                            <link rel="stylesheet" href="/reset.css">
                        </head>
                        <body>
                        <button onclick="topFunction()" id="topBtn" title="Go to top">TOP</button>
                        <div id="wrap">
                            <nav>
                                <div class="logo"><a href="/">#FINDTHESHOP</a></div>
                                <div class="navbar">
                                    <ul>
                                        <li><a href="/">HOME</a></li>
                                        <li><a href="views" target="_self">Product</a></li>
                                    </ul>
                                </div>
                            </nav>
                            <h2 style="text-align:center; margin:30px 0">" ${req.query.query} " 검색 결과입니다</h2>
                            <ul class="Btn">
                                <li class="btn-click"><a href="javascript:sortByDefault()">기본순</a></li>
                                <li class="lowbtn"><a href="sortitemlist?query=${req.query.query}" target="_self">최저가순</a></li>
                            </ul>
                        </div>
                        <div id="wrap">
                        <ul class="item-list">
                    `;
       data.forEach((item) => { 
                        output += `
                            <li class="item">
                                <a href="/iteminfo?productId=${item.productId}" target="_self">
                                    <img src="${item.image}" alt="Product Image">
                                </a>
                                <h4>${item.title}</h4>
                                <p>현재 최저가 <strong style="color:#f56565">${item.lprice}</strong> 원</p>
                            </li>
                        `;
                    });
                    output += `
                                </ul>
                                </div>
                                <script>
                    `;
                    output += `
                                    function sortByDefault() {
                                        window.location.reload();
                                    }
                                    // window 스크롤 이벤트 사용
                                    window.onscroll = function() {scrollFunction()};

                                    function scrollFunction() {
                                    // 스크롤이 20px 이상 내려갔을 때 top 버튼 생성
                                    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
                                        document.getElementById("topBtn").style.display = "block";
                                    } else {
                                        document.getElementById("topBtn").style.display = "none";
                                    }
                                    }

                                    // TOP 버튼을 클릭시 페이지의 맨 위로 이동
                                    function topFunction() {
                                    document.body.scrollTop = 0; // Safari
                                    document.documentElement.scrollTop = 0; // Chrome, Firefox, IE 및 Opera
                                    }
                    `;
                    output += `
                                </script>
                                </body>
                                </html>
                    `;
                    res.send(output);
    } catch (error) {
        console.error(error);
        res.status(500).send('Internal Server Error');
    }
});

// 전체 리스트를 최저가 순으로 출력
app.get('/sortitemlist', async (req, res) => { // req 매개변수 추가
    try {
        const response = await fetch('http://192.168.1.72:3000/sortitemlist');
        const data = await response.json();
        let output = `  
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <meta charset="UTF-8">
                            <title>FINDTHESHOP-상품 조회 결과</title>
                            <link rel="stylesheet" href="/main.css">
                            <link rel="stylesheet" href="/reset.css">
                        </head>
                        <body>
                        <button onclick="topFunction()" id="topBtn" title="Go to top">TOP</button>
                        <div id="wrap">
                            <nav>
                                <div class="logo"><a href="/">#FINDTHESHOP</a></div>
                                <div class="navbar">
                                    <ul>
                                        <li><a href="/">HOME</a></li>
                                        <li><a href="views" target="_self">Product</a></li>
                                    </ul>
                                </div>
                            </nav>
                            <h2 style="text-align:center; margin:30px 0">" ${req.query.query} " 최저가 순 검색 결과입니다</h2>
                            <ul class="Btn">
                                <li class="btn"><a href="deitemlist?query=${req.query.query}" target="_self">기본순</a></li>
                                <li class="lowbtn-click"><a href="javascript:sortByDefault()">최저가순</a></li>
                            </ul>
                        </div>
                        <div id="wrap">
                        <ul class="item-list">
                    `;
       data.forEach((item) => { 
                        output += `
                            <li class="item">
                                <a href="/iteminfo?productId=${item.productId}" target="_self">
                                    <img src="${item.image}" alt="Product Image">
                                </a>
                                <h4>${item.title}</h4>
                                <p>현재 최저가 <strong style="color:#f56565">${item.lprice}</strong> 원</p>
                            </li>
                        `;
                    });
                    output += `
                                </ul>
                                </div>
                                <script>
                    `;
                    output += `
                                    function sortByDefault() {
                                        window.location.reload();
                                    }
                                    // window 스크롤 이벤트 사용
                                    window.onscroll = function() {scrollFunction()};

                                    function scrollFunction() {
                                    // 스크롤이 20px 이상 내려갔을 때 top 버튼 생성
                                    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
                                        document.getElementById("topBtn").style.display = "block";
                                    } else {
                                        document.getElementById("topBtn").style.display = "none";
                                    }
                                    }

                                    // TOP 버튼을 클릭시 페이지의 맨 위로 이동
                                    function topFunction() {
                                    document.body.scrollTop = 0; // Safari
                                    document.documentElement.scrollTop = 0; // Chrome, Firefox, IE 및 Opera
                                    }

                    `;
                    output += `
                                </script>
                                </body>
                                </html>
                    `;
                    res.send(output);
    } catch (error) {
        console.error(error);
        res.status(500).send('Internal Server Error');
    }
});

// 상품 상세 정보 눌렀을 때, mysql mongodb 담기
app.get('/iteminfo', async (req, res) => {
    try {
        const productId = req.query.productId;
        const data = { productId: productId }; 

        const itemResponse = await fetch(`http://192.168.1.72:3000/additem/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const responseItemData = await itemResponse.json();
        const itemList = responseItemData.item;

        const linkResponse = await fetch(`http://192.168.1.72:3000/addlowlink/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const responseLinkData = await linkResponse.json();
        const lowlinklists = responseLinkData.lowlinklist;

        // 상품 정보와 최저가 정보를 HTML에 추가
        let output = `
            <!DOCTYPE html>
            <html lang="ko">
            <head>
                <meta charset="UTF-8">
                <title>FINDTHESHOP-상품 상세 페이지</title>
                <link rel="stylesheet" href="/main.css">
                <link rel="stylesheet" href="/reset.css">
            </head>
            <body>
            <button onclick="topFunction()" id="topBtn" title="Go to top">TOP</button>
                <div id="wrap">
                    <nav>
                        <div class="logo"><a href="/">#FINDTHESHOP</a></div>
                        <div class="navbar">
                            <ul>
                                <li><a href="/">HOME</a></li>
                                <li><a href="views" target="_self">Product</a></li>
                            </ul>
                        </div>
                    </nav>
                </div>
                <div id="wrap">
                    <div class="iteminfo">
                        <div class="img">
                            <img src="${itemList.image}" alt="${itemList.title}">
                        </div>
                        <div class="info">
                            <h3>${itemList.title}</h3>
                            <p>판매처 별 최저가</p>
                            <hr>
                            <ul>
        `;
        
        lowlinklists.forEach(item => {
            output += `
                <li>
                    <a href="${item.link}" alt="최저가링크" target="_blank">
                        <div class="bestlowlink"></div>
                        <div class="shop">${item.shop}</div>
                        <div class="price">${item.price}원</div>
                        <div class="delivery">배송비 ${item.deliveryfee}</div>
                    </a>
                </li>
            `;
        });
        output += `
                            </ul>
                        </div>
                    </div>
                </div>
                <div id="wrap">
                <h2 style="margin-bottom:50px">상품 리뷰</h2>
                <iframe class="iframe-preview center" width="100%" height="2500px" style="border: none;" src="/reviews?productId=${itemList.productId}" frameborder='0' scrolling="no"></iframe>
                </div>
            </body>
            <script>
                // window 스크롤 이벤트 사용
                window.onscroll = function() {scrollFunction()};

                function scrollFunction() {
                // 스크롤이 20px 이상 내려갔을 때 top 버튼 생성
                if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
                    document.getElementById("topBtn").style.display = "block";
                } else {
                    document.getElementById("topBtn").style.display = "none";
                }
                }

                // TOP 버튼을 클릭시 페이지의 맨 위로 이동
                function topFunction() {
                document.body.scrollTop = 0; // Safari
                document.documentElement.scrollTop = 0; // Chrome, Firefox, IE 및 Opera
                }
            </script>
            </html>
        `;
        
        res.send(output);
    } catch (error) {
        console.error(error);
        res.status(500).send('Internal Server Error');
    }
});

// 리뷰 출력 - 다은 api 사용해서 iframe 안에 출력
app.get('/reviews', async (req, res) => {
    try {
        const productId = req.query.productId;
        const reviewResponse = await fetch(`http://192.168.1.162:3500/reviews/${productId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const responseReviewData = await reviewResponse.json();
        const reviewList = responseReviewData.reviews;
        let output = `
                <link rel="stylesheet" href="/main.css">
                <link rel="stylesheet" href="/reset.css">
                `
        reviewList.forEach(item => {
            output += `
                <li class="review-list" style="padding:30px 30px">
                    <div class="rank" style="font-weight:bold; font-size:20px; margin-bottom:10px">⭐ ${item.rank} &nbsp;<span style="font-weight:500; font-size:17px">|&nbsp;${item.date}</span></div>
                    <div class="contents">${item.contents}</div>
                </li>
            `;
        });
        res.send(output);
    } catch (error) {
        console.error(error);
        res.status(500).send('Internal Server Error');
    }
});


module.exports = app;
