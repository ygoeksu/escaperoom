can # Game Engine

Pure Python game logic — no I/O, no framework dependencies. Takes a state in, returns a new state out.

## Concepts

| Concept | Description |
|---|---|
| `GameContent` | Immutable definition of a room scenario (rooms, items, puzzles). Load once. |
| `GameState` | Mutable snapshot of one player's progress (position, inventory, flags). |
| `GameEngine` | Processes commands against a state and returns a new state + message. |
| `ActionResult` | The return value of every command: `(message: str, state: GameState)`. |

---

## Quick Start

```python
from engine import GameEngine, GameContent

# 1. Define your content (or load from JSON)
content = GameContent.model_validate({
    "rooms": {
        "cell_01": {
            "id": "cell_01",
            "name": "Prison Cell",
            "description": "A dark cell with a locked door.",
            "items": ["rusty_key"],
            "exits": {
                "north": {
                    "room_id": "hallway_01",
                    "requires_flag": "door_unlocked",
                    "locked_message": "The door is locked."
                }
            },
            "puzzles": ["door_lock"]
        },
        "hallway_01": {
            "id": "hallway_01",
            "name": "Hallway",
            "description": "A long hallway. You're free!",
            "items": [],
            "exits": {}
        }
    },
    "items": {
        "rusty_key": {
            "id": "rusty_key",
            "name": "rusty key",
            "description": "An old iron key, slightly rusted.",
            "takeable": True
        }
    },
    "puzzles": {
        "door_lock": {
            "id": "door_lock",
            "type": "key_lock",
            "required_item": "rusty_key",
            "result": "door_unlocked",
            "success_message": "The key turns. The door swings open.",
            "failure_message": "That doesn't fit the lock.",
            "consume_item": True
        }
    },
    "start_room": "cell_01",
    "win_condition": {
        "type": "reach_room",
        "room_id": "hallway_01",
        "message": "You escaped!"
    }
})

# 2. Create the engine and start a game
engine = GameEngine(content)
state = engine.new_game()

# 3. Run the game loop
while not state.is_won:
    result = engine.process_command(state, input("> "))
    print(result.message)
    state = result.state
```

---

## Content Schema

### Room

```json
{
  "id": "cell_01",
  "name": "Prison Cell",
  "description": "A dark cell.",
  "items": ["rusty_key"],
  "exits": {
    "north": "hallway_01"
  },
  "puzzles": ["door_lock"]
}
```

Exits can be a plain room ID string **or** a locked exit object:

```json
"exits": {
  "north": {
    "room_id": "hallway_01",
    "requires_flag": "door_unlocked",
    "locked_message": "The door is locked."
  }
}
```

### Item

```json
{
  "id": "rusty_key",
  "name": "rusty key",
  "description": "An old iron key.",
  "takeable": true
}
```

### Puzzle

Two puzzle types are supported:

**`key_lock`** — solved by using an item on it:

```json
{
  "id": "door_lock",
  "type": "key_lock",
  "required_item": "rusty_key",
  "result": "door_unlocked",
  "success_message": "The door opens!",
  "failure_message": "That doesn't fit.",
  "consume_item": true
}
```

**`code`** — solved by entering a code with the `solve` command:

```json
{
  "id": "keypad",
  "type": "code",
  "code": "1234",
  "result": "keypad_unlocked",
  "success_message": "The panel beeps. Access granted.",
  "failure_message": "Wrong code."
}
```

### Win Condition

Trigger win when the player reaches a room:

```json
"win_condition": {
  "type": "reach_room",
  "room_id": "exit_room",
  "message": "You escaped!"
}
```

Or when a specific flag is set:

```json
"win_condition": {
  "type": "have_flag",
  "flag": "safe_opened",
  "message": "You cracked the safe and found the evidence!"
}
```

---

## Commands

| Player types | What it does |
|---|---|
| `look` / `l` | Describe the current room |
| `examine <item>` / `x <item>` | Examine an item in the room or inventory |
| `go north` / `north` / `n` | Move in a direction |
| `take <item>` / `get <item>` | Pick up an item |
| `drop <item>` | Drop an item in the current room |
| `inventory` / `i` | List carried items |
| `use <item>` | Use an item (tries all puzzles in the room) |
| `use <item> on <puzzle>` | Use an item on a specific puzzle |
| `solve <puzzle> <code>` | Enter a code for a code-type puzzle |
| `help` | Show command list |

---4791

## Loading Content from JSON

```python
import json
from engine import GameEngine, GameContent

with open("content/my_room.json") as f:
    data = json.load(f)

content = GameContent.model_validate(data)
engine = GameEngine(content)
state = engine.new_game()
```

---

## How State Works

`GameState` is never mutated in place. Every `process_command` call returns a **new** `GameState`. This makes the engine stateless at the API layer — the API just stores the state between requests.

```python
# state is unchanged after this call
result = engine.process_command(state, "take key")

# use result.state going forward
state = result.state
print(result.message)   # "You take the rusty key."
print(state.inventory)  # ["rusty_key"]
print(state.is_won)     # False
```

Key fields on `GameState`:

| Field | Type | Description |
|---|---|---|
| `current_room_id` | `str` | Room the player is in |
| `inventory` | `list[str]` | Item IDs the player is carrying |
| `solved_puzzles` | `list[str]` | Puzzle IDs that have been solved |
| `flags` | `dict[str, str]` | Key/value flags set by puzzle results |
| `room_items` | `dict[str, list[str]]` | Current items in each room (changes as items are taken/dropped) |
| `is_won` | `bool` | True when the win condition is met |
| `turns` | `int` | Number of commands processed |
