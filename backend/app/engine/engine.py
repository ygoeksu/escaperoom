from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Optional

from .models import GameContent, GameState, LockedExit, Puzzle
from .parser import ParsedCommand, parse_command


@dataclass
class ActionResult:
    message: str
    state: GameState


_Handler = Callable[["GameEngine", GameState, Optional[str], Optional[str]], ActionResult]


class GameEngine:
    def __init__(self, content: GameContent) -> None:
        self.content = content
        self.state = self.new_game()
    # --- public API ---

    def new_game(self) -> GameState:
        room_items = {room_id: list(room.items) for room_id, room in self.content.rooms.items()}
        return GameState(current_room_id=self.content.start_room, room_items=room_items)

    def process_command(self, raw: str) -> ActionResult:
        if self.state.is_won:
            return ActionResult("You have already escaped!", self.state)

        cmd = parse_command(raw)
        state = self.state.model_copy(update={"turns": self.state.turns + 1})

        handlers: dict[str, _Handler] = {
            "look": GameEngine._look,
            "examine": GameEngine._examine,
            "go": GameEngine._go,
            "take": GameEngine._take,
            "drop": GameEngine._drop,
            "inventory": GameEngine._inventory,
            "use": GameEngine._use,
            "solve": GameEngine._solve,
            "help": GameEngine._help,
            "quit": GameEngine._quit,
        }

        handler = handlers.get(cmd.verb)
        if handler is None:
            return ActionResult(f"I don't understand '{cmd.raw}'.", state)

        result = handler(self, state, cmd.noun, cmd.target)
        return self._check_win(result)

    # --- helpers ---

    def _room(self, state: GameState):
        return self.content.rooms[state.current_room_id]

    def _find_item_id(self, name: str) -> Optional[str]:
        name_lower = name.lower()
        for item_id, item in self.content.items.items():
            if item_id.lower() == name_lower or item.name.lower() == name_lower:
                return item_id
        return None

    def _find_puzzle_id(self, name: str, room_puzzles: list[str]) -> Optional[str]:
        name_lower = name.lower()
        for pid in room_puzzles:
            puzzle = self.content.puzzles.get(pid)
            if pid.lower() == name_lower or (puzzle and puzzle.id.lower() == name_lower):
                return pid
        return None

    def _describe_room(self, state: GameState) -> str:
        room = self._room(state)
        lines = [f"**{room.name}**", room.description]

        items_here = state.room_items.get(room.id, [])
        if items_here:
            names = [self.content.items[i].name for i in items_here if i in self.content.items]
            lines.append("You see: " + ", ".join(names) + ".")

        if room.exits:
            exit_labels = []
            for direction, ex in room.exits.items():
                if isinstance(ex, str):
                    exit_labels.append(direction)
                elif state.flags.get(ex.requires_flag):
                    exit_labels.append(direction)
                else:
                    exit_labels.append(f"{direction} (locked)")
            lines.append("Exits: " + ", ".join(exit_labels) + ".")
        else:
            lines.append("There are no obvious exits.")

        return "\n".join(lines)

    def _apply_item_to_puzzle(self, state: GameState, item_id: str, puzzle_id: str) -> ActionResult:
        puzzle = self.content.puzzles.get(puzzle_id)
        if puzzle is None:
            return ActionResult("Nothing happens.", state)
        if puzzle_id in state.solved_puzzles:
            return ActionResult("That's already been done.", state)
        if puzzle.required_item == item_id:
            return self._solve_puzzle(state, puzzle, item_id)
        return ActionResult(puzzle.failure_message, state)

    def _solve_puzzle(self, state: GameState, puzzle: Puzzle, used_item_id: Optional[str]) -> ActionResult:
        new_inventory = (
            [i for i in state.inventory if i != used_item_id]
            if used_item_id and puzzle.consume_item
            else list(state.inventory)
        )
        new_state = state.model_copy(update={
            "solved_puzzles": state.solved_puzzles + [puzzle.id],
            "flags": {**state.flags, puzzle.result: "true"},
            "inventory": new_inventory,
        })
        return ActionResult(puzzle.success_message, new_state)

    def _check_win(self, result: ActionResult) -> ActionResult:
        state = result.state
        win = self.content.win_condition
        won = (
            (win.type == "reach_room" and state.current_room_id == win.room_id)
            or (win.type == "have_flag" and state.flags.get(win.flag) == "true")
        )
        if won:
            new_state = state.model_copy(update={"is_won": True})
            return ActionResult(result.message + "\n\n" + win.message, new_state)
        return result

    # --- action handlers ---

    def _look(self, state: GameState, noun: Optional[str], target: Optional[str]) -> ActionResult:
        return ActionResult(self._describe_room(state), state)

    def _examine(self, state: GameState, noun: Optional[str], target: Optional[str]) -> ActionResult:
        if not noun:
            return ActionResult("Examine what?", state)

        item_id = self._find_item_id(noun)
        if item_id is None:
            return ActionResult(f"You don't see '{noun}' here.", state)

        room = self._room(state)
        in_room = item_id in state.room_items.get(room.id, [])
        in_inv = item_id in state.inventory

        if not in_room and not in_inv:
            return ActionResult(f"You don't see '{noun}' here.", state)

        return ActionResult(self.content.items[item_id].description, state)

    def _go(self, state: GameState, noun: Optional[str], target: Optional[str]) -> ActionResult:
        if not noun:
            return ActionResult("Go where?", state)

        room = self._room(state)
        exit_entry = room.exits.get(noun)

        if exit_entry is None:
            return ActionResult(f"You can't go {noun} from here.", state)

        if isinstance(exit_entry, str):
            dest_id = exit_entry
        else:
            if not state.flags.get(exit_entry.requires_flag):
                return ActionResult(exit_entry.locked_message, state)
            dest_id = exit_entry.room_id

        if dest_id not in self.content.rooms:
            return ActionResult("That path leads nowhere.", state)

        new_state = state.model_copy(update={"current_room_id": dest_id})
        return ActionResult(self._describe_room(new_state), new_state)

    def _take(self, state: GameState, noun: Optional[str], target: Optional[str]) -> ActionResult:
        if not noun:
            return ActionResult("Take what?", state)

        item_id = self._find_item_id(noun)
        room = self._room(state)
        room_items = state.room_items.get(room.id, [])

        if item_id is None or item_id not in room_items:
            return ActionResult(f"There is no '{noun}' here to take.", state)

        item = self.content.items[item_id]
        if not item.takeable:
            return ActionResult(f"You can't take the {item.name}.", state)

        new_state = state.model_copy(update={
            "room_items": {**state.room_items, room.id: [i for i in room_items if i != item_id]},
            "inventory": state.inventory + [item_id],
        })
        return ActionResult(f"You take the {item.name}.", new_state)

    def _drop(self, state: GameState, noun: Optional[str], target: Optional[str]) -> ActionResult:
        if not noun:
            return ActionResult("Drop what?", state)

        item_id = self._find_item_id(noun)
        if item_id is None or item_id not in state.inventory:
            return ActionResult(f"You don't have '{noun}'.", state)

        item = self.content.items[item_id]
        room = self._room(state)
        new_state = state.model_copy(update={
            "inventory": [i for i in state.inventory if i != item_id],
            "room_items": {**state.room_items, room.id: state.room_items.get(room.id, []) + [item_id]},
        })
        return ActionResult(f"You drop the {item.name}.", new_state)

    def _inventory(self, state: GameState, noun: Optional[str], target: Optional[str]) -> ActionResult:
        if not state.inventory:
            return ActionResult("Your inventory is empty.", state)
        names = [self.content.items[i].name for i in state.inventory if i in self.content.items]
        return ActionResult("You are carrying: " + ", ".join(names) + ".", state)

    def _use(self, state: GameState, noun: Optional[str], target: Optional[str]) -> ActionResult:
        if not noun:
            return ActionResult("Use what?", state)

        item_id = self._find_item_id(noun)
        if item_id is None or item_id not in state.inventory:
            return ActionResult(f"You don't have '{noun}'.", state)

        room = self._room(state)

        if target:
            puzzle_id = self._find_puzzle_id(target, room.puzzles)
            if puzzle_id is None:
                return ActionResult(f"There's no '{target}' here to use that on.", state)
            return self._apply_item_to_puzzle(state, item_id, puzzle_id)

        for puzzle_id in room.puzzles:
            puzzle = self.content.puzzles.get(puzzle_id)
            if puzzle and puzzle.required_item == item_id and puzzle_id not in state.solved_puzzles:
                return self._apply_item_to_puzzle(state, item_id, puzzle_id)

        return ActionResult(f"You can't use the {self.content.items[item_id].name} here.", state)

    def _solve(self, state: GameState, noun: Optional[str], target: Optional[str]) -> ActionResult:
        """Handle: solve <puzzle_id> <code>"""
        if not noun:
            return ActionResult("Solve what?", state)

        room = self._room(state)
        parts = noun.split(maxsplit=1)
        puzzle_name = parts[0]
        code_attempt = parts[1] if len(parts) > 1 else (target or "")

        puzzle_id = self._find_puzzle_id(puzzle_name, room.puzzles)
        if puzzle_id is None:
            return ActionResult(f"There's no '{puzzle_name}' puzzle here.", state)

        if puzzle_id in state.solved_puzzles:
            return ActionResult("That puzzle is already solved.", state)

        puzzle = self.content.puzzles[puzzle_id]
        if puzzle.type != "code":
            return ActionResult("You can't solve that by entering a code.", state)

        if puzzle.code and code_attempt == puzzle.code:
            return self._solve_puzzle(state, puzzle, None)

        return ActionResult(puzzle.failure_message, state)

    def _help(self, state: GameState, noun: Optional[str], target: Optional[str]) -> ActionResult:
        return ActionResult(
            "Commands:\n"
            "  look / l               - describe the current room\n"
            "  examine <item>         - examine an item\n"
            "  go <direction>         - move (north/south/east/west/up/down)\n"
            "  take <item>            - pick up an item\n"
            "  drop <item>            - drop an item\n"
            "  inventory / i          - list carried items\n"
            "  use <item>             - use an item in the current room\n"
            "  use <item> on <target> - use an item on a specific puzzle\n"
            "  solve <puzzle> <code>  - enter a code for a code puzzle\n"
            "  help                   - show this message",
            state,
        )

    def _quit(self, state: GameState, noun: Optional[str], target: Optional[str]) -> ActionResult:
        return ActionResult("Thanks for playing!", state)
