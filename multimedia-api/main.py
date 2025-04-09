from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client.multimedia_db

class PlayerScore(BaseModel):
    player_name: str
    score: int

@app.post("/upload_sprite")
async def upload_sprite(file: UploadFile = File(...)):
    content = await file.read()
    doc = {"filename": file.filename, "content": content}
    result = await db.sprites.insert_one(doc)
    return {"message": "Sprite uploaded", "id": str(result.inserted_id)}

@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...)):
    content = await file.read()
    doc = {"filename": file.filename, "content": content}
    result = await db.audio.insert_one(doc)
    return {"message": "Audio uploaded", "id": str(result.inserted_id)}

@app.post("/player_score")
async def add_score(score: PlayerScore):
    doc = score.dict()
    result = await db.scores.insert_one(doc)
    return {"message": "Score saved", "id": str(result.inserted_id)}