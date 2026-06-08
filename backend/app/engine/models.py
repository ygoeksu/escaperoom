from __future__ import annotations
from typing import Optional, Union
from pydantic import BaseModel


class Item(BaseModel):
    id: str
    name: str
    description: str
    takeable: bool = True


class LockedExit(BaseModel):
    room_id: str
    requires_flag: str
    locked_message: str = "The way is blocked."


class Puzzle(BaseModel):
    id: str
    type: str  # "key_lock" | "code"
    required_item: Optional[str] = None
    code: Optional[str] = None
    result: str  # flag name set to "true" on solve
    success_message: str = "It works!"
    failure_message: str = "Nothing happens."
    consume_item: bool = True


class Room(BaseModel):
    id: str
    name: str
    description: str
    items: list[str] = []
    exits: dict[str, Union[str, LockedExit]] = {}
    puzzles: list[str] = []


class WinCondition(BaseModel):
    type: str  # "reach_room" | "have_flag"
    room_id: Optional[str] = None
    flag: Optional[str] = None
    message: str = "You escaped! Congratulations!"


class GameContent(BaseModel):
    rooms: dict[str, Room]
    items: dict[str, Item]
    puzzles: dict[str, Puzzle]
    start_room: str
    win_condition: WinCondition


class GameState(BaseModel):
    current_room_id: str
    inventory: list[str] = []
    solved_puzzles: list[str] = []
    flags: dict[str, str] = {}
    room_items: dict[str, list[str]] = {}
    is_won: bool = False
    turns: int = 0
