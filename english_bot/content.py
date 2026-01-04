from __future__ import annotations
import json, random
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class Entry:
    id: str
    idiom: str
    meaning_ko: str
    example_en: str
    example_ko: str

def load_entries(path: str) -> list[Entry]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []  # 빈 파일
            raw = json.loads(content)
    except FileNotFoundError:
        return []  # 파일 없음
    except json.JSONDecodeError:
        return []  # JSON 파싱 실패

    if not raw or not isinstance(raw, list):
        return []

    # "있다고 가정"한 스키마를 최소한으로 강제
    out = []
    for i, r in enumerate(raw):
        out.append(Entry(
            id=str(r.get("id", f"{path}:{i}")),
            idiom=r["idiom"] if "idiom" in r else r["expression"],
            meaning_ko=r["meaning_ko"],
            example_en=r.get("example_en",""),
            example_ko=r["example_ko"],
        ))
    return out

def pick_next(entries: list[Entry], cursor: int, n: int, used: set[str]) -> tuple[list[Entry], int]:
    picked = []
    i = cursor
    checked = 0  # 무한루프 방지: 전체 entry 수만큼만 체크
    
    # 순회하면서 used에 없는 것만 pick
    while len(picked) < n and checked < len(entries):
        e = entries[i % len(entries)]
        if e.id not in used:
            picked.append(e)
            used.add(e.id)
        i += 1
        checked += 1
    
    # 새로 뽑을 게 없으면 (모두 used) 처음부터 다시
    if not picked and entries:
        print("[DEBUG] All entries used, resetting for new cycle...")
        for j in range(min(n, len(entries))):
            picked.append(entries[(cursor + j) % len(entries)])
        i = cursor + len(picked)
    
    return picked, (i % len(entries))

def pick_random(entries: list[Entry], k: int, seed: str | None = None) -> list[Entry]:
    rng = random.Random(seed)
    if k >= len(entries): 
        return entries[:]
    return rng.sample(entries, k)
