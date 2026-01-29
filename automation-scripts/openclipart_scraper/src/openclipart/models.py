from dataclasses import dataclass


@dataclass(frozen=True)
class ClipartInfo:
    title: str
    author: str
    svg_url: str
    small_png_url: str
    medium_png_url: str
    large_png_url: str
    base_filename: str
