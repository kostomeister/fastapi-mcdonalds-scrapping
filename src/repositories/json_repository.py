import json
from typing import Dict, List, Optional


class JSONRepository:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    async def get_one(self, name: str) -> Optional[Dict[str, str]]:
        data = await self._load_data()
        for product_id, product_data in data.items():
            if product_data.get('name', '').lower() == name.lower():
                return {**product_data, "id": product_id}
        return None

    async def get_all(self) -> dict[str, dict]:
        return await self._load_data()

    async def _load_data(self) -> Dict[str, dict]:
        try:
            with open(self.file_path, 'r', encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
