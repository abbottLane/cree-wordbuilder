# It's a backend!
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.websockets import WebSocket
import json
import os
import app.autocomplete as autocomplete
import logging 

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


@app.get("/")
def read_root():
    return "Oh, hello there. Nothing to see here."


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print('websocket connected')
    while True:
        data = await websocket.receive_json()
        if (data['type'] == 'ping'):
            await websocket.send_json({'type': 'pong'})
        elif (data['type'] == 'search'):
            results, totalcount, analysis = await autocomplete.search(data['data'])
            await websocket.send_json({'type': 'results', 'data': {'results': results, 'total': totalcount, 'analysis': analysis}})
        
