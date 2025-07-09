import json
import logging
from pathlib import Path
from typing import List, Dict

import aiofiles

from src.data.interfaces import IProductRepository


logger = logging.getLogger(__name__)


class JSONRepo(IProductRepository):
    def __init__(self, path: Path):
        self._path = path

    async def read_all(self) -> List[Dict]:
        try:
            async with aiofiles.open(self._path, "r", encoding="utf-8") as f:
                logger.info("Reading data from %s", self._path)
                return json.loads(await f.read())
        except FileNotFoundError:
            logger.warning("File %s not found, returning empty list", self._path)
            return []

    async def write_all(self, data: List[Dict]) -> None:
        async with aiofiles.open(self._path, "w", encoding="utf-8") as f:
            logger.info("Writing %d products to %s", len(data), self._path)
            await f.write(json.dumps(data, ensure_ascii=False, indent=4))
