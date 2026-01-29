from pathlib import Path
import yaml


class AppConfig:
    def __init__(self, path: str):
        data = yaml.safe_load(Path(path).read_text())

        self.download_dir = Path(data["download_dir"])
        self.urls = data.get("urls", [])
        self.ssl_verify = bool(data.get("ssl_verify", True))

        self.download_dir.mkdir(parents=True, exist_ok=True)
