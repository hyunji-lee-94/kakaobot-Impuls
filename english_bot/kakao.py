import json
import subprocess
import requests
from typing import Optional

KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_MEMO_SEND_URL = "https://kapi.kakao.com/v2/api/talk/memo/default/send"


def update_infisical_secret(secret_name: str, secret_value: str, env: str = "prod", path: str = "/KAKAO") -> bool:
    """Infisical에 secret 업데이트"""
    try:
        result = subprocess.run(
            ["infisical", "secrets", "set", f"{secret_name}={secret_value}", 
             "--env", env, "--path", path],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print(f"✅ Infisical 업데이트 완료: {secret_name}")
            return True
        else:
            print(f"❌ Infisical 업데이트 실패: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Infisical 업데이트 오류: {e}")
        return False


class KakaoClient:
    def __init__(self, rest_api_key: str, refresh_token: str, client_secret: Optional[str] = None):
        self.rest_api_key = rest_api_key
        self.refresh_token = refresh_token
        self.client_secret = client_secret

    def refresh_access_token(self) -> str:
        payload = {
            "grant_type": "refresh_token",
            "client_id": self.rest_api_key,
            "refresh_token": self.refresh_token,
        }
        if self.client_secret:
            payload["client_secret"] = self.client_secret

        r = requests.post(KAKAO_TOKEN_URL, data=payload, timeout=30)
        r.raise_for_status()
        data = r.json()
        
        # 새 refresh_token이 발급되면 Infisical에 자동 업데이트
        if "refresh_token" in data:
            new_token = data["refresh_token"]
            print(f"🔄 새 refresh_token 발급됨, Infisical 업데이트 중...")
            update_infisical_secret("KAKAO_REFRESH_TOKEN", new_token)
            self.refresh_token = new_token
        
        return data["access_token"]

    def send_memo_default(self, access_token: str, template_object: dict) -> dict:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        data = {"template_object": json.dumps(template_object, ensure_ascii=False)}
        r = requests.post(KAKAO_MEMO_SEND_URL, headers=headers, data=data, timeout=30)
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
