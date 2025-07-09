from typing import Protocol, List, Dict


class IFetcher(Protocol):
    async def fetch(self, url: str) -> str: ...


class IParser(Protocol):
    def extract_links(self, html: str) -> List[str]: ...
    def parse(self, html: str) -> Dict: ...


class IScraper(Protocol):
    async def scrape(self) -> List[Dict]: ...
