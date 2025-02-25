from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from sqlmodel import Session
from database import engine

import uvicorn

from os import environ

app = FastAPI()
session = Session(bind=engine)

#routes
# a simple HTML response
@app.get('/', response_class=HTMLResponse)
async def home():
    return '''
    <h1> Welcome to Antony's bank </h1>
    '''

# a java script response for basic information
@app.get('/info')
def info():
    return {
        'version': "0.1.0",
        'user': environ['USER']
    }

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)