from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}
