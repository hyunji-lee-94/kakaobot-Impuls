import datetime as dt
import random
from zoneinfo import ZoneInfo
from .content import Entry

_WEEKDAYS_EN = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def header_date(tz: str) -> str:
    now = dt.datetime.now(ZoneInfo(tz))
    return f"{_WEEKDAYS_EN[now.weekday()]}, {now.strftime('%B')} {now.day}, {now.year}"

def morning_message(tz: str, items: list[Entry]) -> str:
    """Morning vocabulary delivery"""
    lines = [
        f"📚 Daily Expressions",
        f"{header_date(tz)}",
        "─" * 20,
        ""
    ]
    
    for i, e in enumerate(items, 1):
        lines.append(f"▸ {e.idiom}")
        lines.append(f"  → {e.meaning_ko}")
        lines.append("")
        if e.example_en:
            lines.append(f"  📝 {e.example_en}")
        lines.append(f"  💬 {e.example_ko}")
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
    
    # Extract examples, shuffle, limit to count
    examples = [(e.example_ko, e.idiom) for e in items if e.example_ko]
    random.shuffle(examples)
    examples = examples[:min(count, len(examples))]
    
    for i, (ex_ko, idiom) in enumerate(examples, 1):
        lines.append(f"{i}. {ex_ko}")
    
    lines.append("")
    lines.append("─" * 20)
    lines.append("📖 Answers:")
    for i, (ex_ko, idiom) in enumerate(examples, 1):
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
    
    # 3 quiz types
    quiz_types = ["ko", "en", "idiom"]
    quizzes = []
    
    for e in items:
        qtype = random.choice(quiz_types)
        if qtype == "ko" and e.example_ko:
            quizzes.append(("ko", e.example_ko, e.idiom, e.meaning_ko))
        elif qtype == "en" and e.example_en:
            quizzes.append(("en", e.example_en, e.idiom, e.meaning_ko))
        else:
            quizzes.append(("idiom", e.idiom, e.meaning_ko, e.example_ko))
    
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
