from fastapi import FastAPI
import json
from pydantic import BaseModel
from engine.engine import GameEngine, GameContent
from pathlib import Path

app = FastAPI(title="Escape Room Engine")
BASE_DIR = Path(__file__).resolve().parent
ROOMS_DIR = BASE_DIR / "content"
sessions = {}


class CommandRequest(BaseModel):
    user_input: str

class StartRequest(BaseModel):    room_name: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/options")
async def options():
    return {
        "games": [
            room.stem
            for room in ROOMS_DIR.glob("*.json")
        ]
    }

@app.post("/start/{user_id}")
async def start(user_id: str, req: StartRequest):
    room_file = ROOMS_DIR / f"{req.room_name}.json"
    with room_file.open() as f:
        content = GameContent.model_validate(json.load(f))

    engine = GameEngine(content)
    sessions[user_id] = engine
    return sessions[user_id].state

@app.post("/command/{user_id}")
def command(user_id: str, req: CommandRequest):
    e = sessions[user_id]

    result = e.process_command(req.user_input)
    e.state = result.state

    return {
        "message": result.message,
        "state": result.state,
        "is_won": result.state.is_won
    }
