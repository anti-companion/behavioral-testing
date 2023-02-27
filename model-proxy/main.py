import torch
from models.pygmalion import PygmalionProxy, PygmalionResponse, PygmalionRequest
from settings import Settings

from fastapi import FastAPI
import logging

logging.basicConfig(level=logging.INFO)

settings = Settings()

model_proxy = PygmalionProxy(settings.model_name)

app = FastAPI(debug=True)


@app.post("/greeting")
def greeting(request: PygmalionRequest) -> PygmalionResponse:
    response = model_proxy.get_greeting(request)
    return response


@app.post("/generate")
def generate(request: PygmalionRequest) -> PygmalionResponse:
    response = model_proxy.generate(request)
    return response
