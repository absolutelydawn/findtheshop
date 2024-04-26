json:
	nodemon --watch items.json --exec json-server items.json --port 5000 &
app:
	uvicorn app:app --host 0.0.0.0 --port 3000 --reload &