#!usr/bin/env python
#!usr/bin/env python
import uvicorn
from fastapi import FastAPI
app = FastAPI()
import requests
@app.get("/")
def read_root():
    return {"Hello":"World"}

base_url = 'http://192.168.1.72:5000/items'
@app.get(path='/items')
def getItems():
    reponse = requests.get(base_url)
    return reponse.json()


if __name__=='__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)