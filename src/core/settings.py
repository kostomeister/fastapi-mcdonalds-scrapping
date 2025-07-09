from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "McD Menu API (N-layer)"
    json_path: Path = _ROOT / "mcdonalds_menu.json"
    scraper_timeout_ms: int = 30_000
    scraper_concurrency: int = 12
    base_url: str = "https://www.mcdonalds.com/"
    detail_anchor: str = "#accordion-29309a7a60-item-9ea8a10642"
    headless: bool = False
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )


settings = Settings()
