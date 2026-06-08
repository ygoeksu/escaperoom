from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

DIRECTION_ALIASES: dict[str, str] = {
    "n": "north", "s": "south", "e": "east", "w": "west", "u": "up", "d": "down",
}

VERB_ALIASES: dict[str, str] = {
    "l": "look",
    "i": "inventory",
    "inv": "inventory",
    "get": "take",
    "grab": "take",
    "pick": "take",
    "inspect": "examine",
    "ex": "examine",
    "x": "examine",
    "q": "quit",
}

BARE_DIRECTIONS: frozenset[str] = frozenset(DIRECTION_ALIASES) | frozenset(DIRECTION_ALIASES.values())


@dataclass
class ParsedCommand:
    verb: str
    noun: Optional[str] = field(default=None)
    target: Optional[str] = field(default=None)
    raw: str = field(default="")


def parse_command(raw: str) -> ParsedCommand:
    text = raw.strip().lower()

    if not text:
        return ParsedCommand(verb="", raw=raw)

    # bare direction shortcut
    if text in BARE_DIRECTIONS:
        direction = DIRECTION_ALIASES.get(text, text)
        return ParsedCommand(verb="go", noun=direction, raw=raw)

    parts = text.split()
    verb = VERB_ALIASES.get(parts[0], parts[0])

    if verb == "go":
        direction = DIRECTION_ALIASES.get(parts[1], parts[1]) if len(parts) >= 2 else None
        return ParsedCommand(verb="go", noun=direction, raw=raw)

    # "look at <thing>" -> examine <thing>
    if verb == "look" and len(parts) >= 2 and parts[1] == "at":
        noun = " ".join(parts[2:]) if len(parts) > 2 else None
        return ParsedCommand(verb="examine", noun=noun, raw=raw)

    # "use <item> on <target>"
    if verb == "use" and "on" in parts:
        on_idx = parts.index("on")
        noun = " ".join(parts[1:on_idx]) or None
        target = " ".join(parts[on_idx + 1:]) or None
        return ParsedCommand(verb="use", noun=noun, target=target, raw=raw)

    noun = " ".join(parts[1:]) or None
    return ParsedCommand(verb=verb, noun=noun, raw=raw)
