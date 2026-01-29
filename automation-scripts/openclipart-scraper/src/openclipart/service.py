import asyncio
import aiohttp
from openclipart.http_client import AsyncHttpClient
from openclipart.parser import OpenClipartParser
from openclipart.models import ClipartInfo
from helper.utils import slugify
from helper.logger import *


class OpenClipartService:
    def __init__(self, download_dir, ssl_verify: bool = True):
        self.client = AsyncHttpClient(ssl_verify)
        self.download_dir = download_dir

    async def process_url(self, session, url: str) -> ClipartInfo:
        html = await self.client.fetch_text(session, url)
        parser = OpenClipartParser(html)

        title, author = parser.extract_title_author()
        links = parser.extract_links()

        base = f"{slugify(author)}-{slugify(title)}"
        files = {
            "svg": (links["svg"], f"{base}.svg"),
            "small": (links["small"], f"{base}__small.png"),
            "medium": (links["medium"], f"{base}__medium.png"),
            "large": (links["large"], f"{base}__large.png"),
        }

        if True:
            for url, name in files.values():
                await self.client.download(
                    session,
                    url,
                    self.download_dir / name,
                )

        return ClipartInfo(
            title=title,
            author=author,
            svg_url=links["svg"],
            small_png_url=links["small"],
            medium_png_url=links["medium"],
            large_png_url=links["large"],
            base_filename=base,
        )

    async def run(self, urls: list[str]):
        async with aiohttp.ClientSession() as session:
            return await asyncio.gather(
                *(self.process_url(session, u) for u in urls)
            )
