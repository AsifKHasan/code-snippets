from bs4 import BeautifulSoup
from openclipart.exceptions import ParsingError
from helper.logger import *


class OpenClipartParser:
    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, "html.parser")

    def extract_title_author(self) -> tuple[str, str]:
        h2 = self.soup.find("h2")
        if not h2:
            raise ParsingError("Title not found")

        title = h2.get_text(strip=True)

        author = 'unknown'
        author_link = self.soup.select_one('a[href*="/artist/"]')
        if author_link:
            author = author_link.get_text()

        return title, author

    def extract_links(self) -> dict[str, str]:
        links = {}
        url_prefix = 'https://openclipart.org'
        for a in self.soup.select("a[href]"):
            label = a.get_text(strip=True)
            if label == "Download SVG":
                links["svg"] = url_prefix + a["href"]
            elif label in {"Small", "Medium", "Large"}:
                links[label.lower()] = url_prefix + a["href"]

        required = {"svg", "small", "medium", "large"}
        if not required.issubset(links):
            raise ParsingError("Missing download links")

        return links
