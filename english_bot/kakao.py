import json
import requests
from typing import Optional

KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_MEMO_SEND_URL = "https://kapi.kakao.com/v2/api/talk/memo/default/send"


class KakaoClient:
    def __init__(self, rest_api_key: str, refresh_token: str, client_secret: Optional[str] = None):
        self.rest_api_key = rest_api_key
        self.refresh_token = refresh_token
        self.client_secret = client_secret

    def refresh_access_token(self) -> str:
        print("[DEBUG] refresh_access_token() called")
        payload = {
            "grant_type": "refresh_token",
            "client_id": self.rest_api_key,
            "refresh_token": self.refresh_token,
        }
        if self.client_secret:
            payload["client_secret"] = self.client_secret

        print("[DEBUG] Sending request to Kakao...")
        r = requests.post(KAKAO_TOKEN_URL, data=payload, timeout=30)
        print(f"[DEBUG] Response status: {r.status_code}")
        r.raise_for_status()
        data = r.json()
        print("[DEBUG] Token response received")
        
        # 새 refresh_token이 발급되면 경고만 출력 (토큰 값은 보안상 출력 안 함)
        if "refresh_token" in data:
            print("=" * 60)
            print("⚠️  새 refresh_token이 발급되었습니다!")
            print("    로컬에서 다시 실행하여 Infisical을 업데이트하세요.")
            print("=" * 60)
            self.refresh_token = data["refresh_token"]
        
        return data["access_token"]

    def send_memo_default(self, access_token: str, template_object: dict) -> dict:
        print("[DEBUG] send_memo_default() called")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        data = {"template_object": json.dumps(template_object, ensure_ascii=False)}
        print("[DEBUG] Sending memo to Kakao...")
        r = requests.post(KAKAO_MEMO_SEND_URL, headers=headers, data=data, timeout=30)
        print(f"[DEBUG] Memo response status: {r.status_code}")
        r.raise_for_status()
        return r.json()

    def send_text(self, access_token: str, text: str) -> dict:
        """텍스트 메시지를 나에게 보내기"""
        template_object = {
            "object_type": "text",
            "text": text,
            "link": {
                "web_url": "",
                "mobile_web_url": ""
            }
        }
        return self.send_memo_default(access_token, template_object)
