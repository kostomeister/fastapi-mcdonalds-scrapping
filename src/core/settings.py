from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "McD Menu API (N-layer)"
    json_path: Path = Path("./mcd_menu.json")
    scraper_timeout_ms: int = 30_000
    scraper_concurrency: int = 4
    base_url: str = "https://www.mcdonalds.com/"
    detail_anchor: str = "#accordion-29309a7a60-item-9ea8a10642"
    headless: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)


settings = Settings()
