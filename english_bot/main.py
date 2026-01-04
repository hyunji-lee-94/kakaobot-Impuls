# app/main.py (핵심 부분만)
import argparse
import datetime as dt
from zoneinfo import ZoneInfo

from .config import load_settings
from .kakao import KakaoClient
from .content import load_entries, pick_next
from .state import load_state, save_state
from .templates import morning_message, night_examples_ko, month_end_quiz

def month_key(tz: str) -> str:
    now = dt.datetime.now(ZoneInfo(tz))
    return f"{now.year}{now.month:02d}"

def is_month_end(tz: str) -> bool:
    d = dt.datetime.now(ZoneInfo(tz)).date()
    return (d + dt.timedelta(days=1)).month != d.month

def entries_by_id(entries):
    return {e.id: e for e in entries}

def process_track(track: str, mode: str, entries, tstate, tz: str, kakao: KakaoClient, access: str):
    # 데이터가 비어있으면 안내 메시지 전송
    if not entries:
        kakao.send_text(access, f"[{track.upper()}] ⚠️ 데이터가 비어있습니다. input data를 입력해주세요.")
        return

    id_map = entries_by_id(entries)

    if mode == "morning":
        used = set(tstate.history_ids)
        picked, new_cursor = pick_next(entries, tstate.cursor, 4, used)
        tstate.cursor = new_cursor
        tstate.yesterday_ids = tstate.today_ids
        tstate.today_ids = [e.id for e in picked]
        tstate.history_ids = list(used)

        msg = morning_message(tz, picked)
        kakao.send_text(access, f"[{track.upper()}]\n{msg}")
        return

    if mode == "night":
        import random
        # 역대 전체에서 랜덤 추출
        all_history_ids = list(set(tstate.history_ids or []))
        all_items = [id_map[i] for i in all_history_ids if i in id_map]
        random.shuffle(all_items)

        if is_month_end(tz):
            # 월말 퀴즈: 역대 전체에서 랜덤 출제 (최대 10개)
            quiz_items = all_items[:min(10, len(all_items))]
            msg = month_end_quiz(tz, quiz_items)
        else:
            # 일반 night: 역대 전체에서 랜덤 복습 (최대 6개)
            review_items = all_items[:min(6, len(all_items))]
            msg = night_examples_ko(tz, review_items, count=6)

        kakao.send_text(access, f"[{track.upper()}]\n{msg}")
        return

    raise ValueError("mode must be morning|night")

def run(mode: str):
    s = load_settings()
    st = load_state(s.state_path)

    ym = month_key(s.timezone)
    path_c = f"{s.idiom_dir}/c_idioms_{ym}.json"
    path_b = f"{s.idiom_dir}/b_idioms_{ym}.json"

    entries_c = load_entries(path_c)
    entries_b = load_entries(path_b)

    kakao = KakaoClient(s.kakao_rest_api_key, s.kakao_refresh_token, s.kakao_client_secret)
    access = kakao.refresh_access_token()

    # ✅ 낮/밤 모두 C 따로, B 따로 전송
    process_track("c", mode, entries_c, st.c, s.timezone, kakao, access)
    process_track("b", mode, entries_b, st.b, s.timezone, kakao, access)

    save_state(s.state_path, st)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=["morning","night"])
    run(ap.parse_args().mode)

if __name__ == "__main__":
    main()
