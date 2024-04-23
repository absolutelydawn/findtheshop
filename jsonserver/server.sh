#!/bin/bash

pid=$(lsof -t -i :5000)

if [ -n "$pid" ]; then
    pm2 delete my-json-server
fi
pm2 start json-server --watch db.json --name my-json-server -- --port 5000 &

# fastapi
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &