import json
import urllib
from typing import Dict, Optional


class JSONRepository:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    async def get_one(self, name: str) -> str | None:
        data = await self._load_data()
        name = urllib.parse.unquote(name)
        for product_data in data:
            if product_data.get('Назва', '').lower() == name.lower():
                return product_data
        return None

    async def get_all(self) -> dict[str, dict]:
        return await self._load_data()

    async def _load_data(self) -> Dict[str, dict]:
        try:
            with open(self.file_path, 'r', encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
