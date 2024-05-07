all:
	nodemon --watch items.json --exec json-server items.json --port 5000 &
	uvicorn app:app --host 0.0.0.0 --port 3000 --reload &

kill:
	kill -9 `lsof -t -i :5000`
	kill -9 `lsof -t -i :3000`