import json
from typing import Dict


class JSONRepository:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    async def get_one(self, id: int):
        data = await self._load_data()
        return data.get(str(id))

    async def get_all(self):
        data = await self._load_data()
        return list(data.values())

    async def create_one(self, data: dict):
        current_data = await self._load_data()
        max_id = max(map(int, current_data.keys()), default=0)
        new_id = max_id + 1
        data['id'] = new_id
        current_data[str(new_id)] = data
        await self._save_data(current_data)
        return data

    async def update_one(self, id: int, data: dict):
        current_data = await self._load_data()
        if str(id) not in current_data:
            raise ValueError(f"Object with id {id} does not exist.")
        current_data[str(id)].update(data)
        await self._save_data(current_data)
        return current_data[str(id)]

    async def delete_one(self, id: int):
        current_data = await self._load_data()
        if str(id) not in current_data:
            raise ValueError(f"Object with id {id} does not exist.")
        del current_data[str(id)]
        await self._save_data(current_data)

    async def _load_data(self) -> Dict[str, dict]:
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    async def _save_data(self, data: Dict[str, dict]) -> None:
        with open(self.file_path, 'w') as file:
            json.dump(data, file)
