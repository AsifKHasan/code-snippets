import argparse
import asyncio
import json
from helper.config import AppConfig
from helper.logger import *
from openclipart.service import OpenClipartService


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--url", action="append")
    parser.add_argument("--json", action="store_true")

    args = parser.parse_args()
    config = AppConfig(args.config)

    urls = args.url or config.urls
    if not urls:
        raise SystemExit("No URLs provided")

    service = OpenClipartService(
        config.download_dir,
        ssl_verify=config.ssl_verify,
    )
    results = asyncio.run(service.run(urls))

    if args.json:
        print(json.dumps([r.__dict__ for r in results], indent=2))
    else:
        for r in results:
            print(r.base_filename)


if __name__ == "__main__":
    main()
