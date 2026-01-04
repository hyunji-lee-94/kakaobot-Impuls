# app/state.py
import json
from dataclasses import dataclass, asdict
from typing import Dict, List

@dataclass
class TrackState:
    cursor: int = 0
    today_ids: List[str] = None
    yesterday_ids: List[str] = None
    history_ids: List[str] = None
    def __post_init__(self):
        self.today_ids = self.today_ids or []
        self.yesterday_ids = self.yesterday_ids or []
        self.history_ids = self.history_ids or []

@dataclass
class State:
    c: TrackState = None
    b: TrackState = None
    meta: Dict = None
    def __post_init__(self):
        self.c = self.c if isinstance(self.c, TrackState) else TrackState(**(self.c or {}))
        self.b = self.b if isinstance(self.b, TrackState) else TrackState(**(self.b or {}))
        self.meta = self.meta or {}

def load_state(path: str) -> State:
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content or content == "{}":
                return State(c=TrackState(), b=TrackState(), meta={})
            data = json.loads(content)
            if not data:
                return State(c=TrackState(), b=TrackState(), meta={})
            return State(**data)
    except (FileNotFoundError, json.JSONDecodeError):
        return State(c=TrackState(), b=TrackState(), meta={})

def save_state(path: str, st: State) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(st), f, ensure_ascii=False, indent=2)
