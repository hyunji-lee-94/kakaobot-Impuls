from dataclasses import dataclass
from typing import Optional
import os

@dataclass(frozen=True)
class Settings:
    kakao_rest_api_key: str
    kakao_refresh_token: str
    kakao_client_secret: Optional[str]
    idiom_dir: str
    state_path: str
    timezone: str

def load_settings() -> Settings:
    return Settings(
        kakao_rest_api_key=os.environ["KAKAO_REST_API_KEY"],
        kakao_refresh_token=os.environ["KAKAO_REFRESH_TOKEN"],
        kakao_client_secret=os.getenv("KAKAO_CLIENT_SECRET"),
        idiom_dir=os.getenv("IDIOM_DIR", "data/english-data"),
        state_path=os.getenv("STATE_PATH", "data/english-data/state/state.json"),
        timezone=os.getenv("TZ", "Asia/Seoul"),
    )

