import datetime as dt
import random
from zoneinfo import ZoneInfo
from .content import Entry

_WEEKDAYS_EN = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def header_date(tz: str) -> str:
    now = dt.datetime.now(ZoneInfo(tz))
    return f"{_WEEKDAYS_EN[now.weekday()]}, {now.strftime('%B')} {now.day}, {now.year}"

def morning_message(tz: str, items: list[Entry], max_examples: int = 2) -> str:
    """Morning vocabulary delivery"""
    lines = [
        f"📚 Daily Expressions",
        f"{header_date(tz)}",
        "─" * 15,
        ""
    ]
    
    for i, e in enumerate(items, 1):
        lines.append(f"▸ {e.idiom}")
        lines.append(f"  → {e.meaning_ko}")
        lines.append("")
        
        # 예문 max_examples개만 출력
        for j, ex in enumerate(e.examples[:max_examples], 1):
            if ex.en:
                lines.append(f"  📝 {ex.en}")
            if ex.ko:
                lines.append(f"  💬 {ex.ko}")
            if j < min(len(e.examples), max_examples):
                lines.append("")  # 예문 사이 구분
        lines.append("")
    
    return "\n".join(lines).strip()

def night_examples_ko(tz: str, items: list[Entry], count: int = 6) -> str:
    """Evening review quiz - Korean sentences"""
    lines = [
        f"🌙 Evening Review",
        f"{header_date(tz)}",
        "─" * 20,
        "",
        "Match the Korean sentence to the correct expression:",
        ""
    ]
    
    # 모든 예문 수집 (각 entry의 모든 examples에서)
    all_examples = []
    for e in items:
        for ex in e.examples:
            if ex.ko:
                all_examples.append((ex.ko, e.idiom))
    
    # 랜덤 셔플 후 count개 선택
    random.shuffle(all_examples)
    selected = all_examples[:min(count, len(all_examples))]
    
    if not selected:
        lines.append("No review items available.")
        return "\n".join(lines).strip()
    
    for i, (ex_ko, idiom) in enumerate(selected, 1):
        lines.append(f"{i}. {ex_ko}")
    
    lines.append("")
    lines.append("─" * 20)
    lines.append("📖 Answers:")
    for i, (ex_ko, idiom) in enumerate(selected, 1):
        lines.append(f"{i}. {idiom}")
    
    return "\n".join(lines).strip()

def month_end_quiz(tz: str, items: list[Entry]) -> str:
    """Monthly review quiz - mixed format"""
    lines = [
        f"📝 Monthly Review Quiz",
        f"{header_date(tz)}",
        "─" * 20,
        ""
    ]
    
    if not items:
        lines.append("No quiz data available.")
        return "\n".join(lines).strip()
    
    # 모든 예문 수집
    all_examples = []
    for e in items:
        for ex in e.examples:
            all_examples.append((e.idiom, e.meaning_ko, ex.en, ex.ko))
    
    # 3 quiz types: ko→exp, en→exp, exp→def
    quiz_types = ["ko", "en", "idiom"]
    quizzes = []
    
    for idiom, meaning, ex_en, ex_ko in all_examples:
        qtype = random.choice(quiz_types)
        if qtype == "ko" and ex_ko:
            quizzes.append(("ko", ex_ko, idiom, meaning))
        elif qtype == "en" and ex_en:
            quizzes.append(("en", ex_en, idiom, meaning))
        else:
            quizzes.append(("idiom", idiom, meaning, ex_ko))
    
    random.shuffle(quizzes)
    quizzes = quizzes[:min(8, len(quizzes))]
    
    answers = []
    for i, q in enumerate(quizzes, 1):
        qtype, question, answer, hint = q
        if qtype == "ko":
            lines.append(f"Q{i}. [KO→EXP] {question}")
            answers.append(f"{i}. {answer}")
        elif qtype == "en":
            lines.append(f"Q{i}. [EN→EXP] {question}")
            answers.append(f"{i}. {answer}")
        else:
            lines.append(f"Q{i}. [EXP→DEF] {question}")
            answers.append(f"{i}. {answer}")
    
    lines.append("")
    lines.append("─" * 20)
    lines.append("📖 Answers:")
    lines.extend(answers)
    
    return "\n".join(lines).strip()
