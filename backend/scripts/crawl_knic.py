"""Run from backend: python scripts/crawl_knic.py --output data/knic.txt"""

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.knic_crawler import crawl_knic


async def main():
    parser = argparse.ArgumentParser(description="Export KNIC website content as UTF-8 text")
    parser.add_argument("--max-pages", type=int, default=30)
    parser.add_argument("--max-depth", type=int, default=2)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    filename, content = await crawl_knic(args.max_pages, args.max_depth)
    destination = args.output or Path(filename)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)
    print(destination.resolve())


if __name__ == "__main__":
    asyncio.run(main())
