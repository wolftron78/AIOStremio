import os
import httpx
from fastapi import HTTPException
from typing import Dict

from utils.config import config
from utils.logger import logger

from .base import StreamingService

class TorrentioService(StreamingService):
    def __init__(self):
        self.base_url = "https://torrentio.strem.fun"
        self.debrid_api_key = config.get_addon_debrid_api_key("torrentio")
        self.debrid_service = config.get_addon_debrid_service("torrentio")
        self.options = f"debridoptions=nocatalog|{self.debrid_service}={self.debrid_api_key}"

    @property
    def name(self) -> str:
        return "Torrentio"

    async def _fetch_from_torrentio(self, url: str) -> Dict:
        proxy_url = os.getenv("ADDON_PROXY")
        transport = None
        
        if proxy_url:
            # Modern httpx proxy configuration (0.28+)
            transport = httpx.AsyncHTTPTransport(proxy=proxy_url)
        
        async with httpx.AsyncClient(transport=transport) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                logger.debug(f"Torrentio response: {data}")
                return data
            except httpx.HTTPError as e:
                logger.error(f"Torrentio request failed: {str(e)}")
                raise HTTPException(status_code=502, detail="Upstream service error")
