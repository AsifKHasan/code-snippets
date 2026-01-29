import ssl
from openclipart.exceptions import NetworkError
from helper.logger import *


class AsyncHttpClient:
    def __init__(self, ssl_verify: bool = True):
        self.ssl_context = None
        if not ssl_verify:
            self.ssl_context = ssl.create_default_context()
            self.ssl_context.check_hostname = False
            self.ssl_context.verify_mode = ssl.CERT_NONE

    async def fetch_text(self, session, url: str) -> str:
        try:
            async with session.get(url, ssl=self.ssl_context, timeout=15) as resp:
                resp.raise_for_status()
                return await resp.text()
        except Exception as exc:
            raise NetworkError(f"Failed to fetch {url}") from exc

    async def download(self, session, url: str, target):
        async with session.get(url, ssl=self.ssl_context) as resp:
            resp.raise_for_status()
            target.write_bytes(await resp.read())
