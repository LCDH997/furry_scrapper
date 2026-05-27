from pathlib import Path

import aiohttp

from scrapers.base import BaseScraper
from utils.downloader import download_file
from utils.hashing import Hashing
from utils.metadata import MetadataWriter


class E621Scraper(BaseScraper):
    API_URL = "https://e621.net/posts.json"

    def __init__(self, user_agent, output_root, metadata_root, limit):
        self.headers = {
            "User-Agent": user_agent
        }

        self.output_root = Path(output_root)
        self.metadata_root = Path(metadata_root)
        self.limit = limit

    async def scrape_species(self, species: str):
        downloaded = 0
        page = 1

        async with aiohttp.ClientSession(headers=self.headers) as session:
            while downloaded < self.limit:
                params = {
                    "tags": f"{species} rating:safe",
                    "limit": 100,
                    "page": page,
                }

                async with session.get(self.API_URL, params=params) as response:
                    if response.status != 200:
                        break

                    data = await response.json()
                    posts = data.get("posts", [])

                    if not posts:
                        break

                    for post in posts:
                        file_info = post.get("file")

                        if not file_info:
                            continue

                        image_url = file_info.get("url")

                        if not image_url:
                            continue

                        ext = file_info.get("ext", "jpg")
                        allowed_extensions = {
                            "jpg",
                            "jpeg",
                            "png",
                            "webp",
                        }

                        if ext.lower() not in allowed_extensions:
                            continue
                        post_id = post["id"]

                        image_path = (
                            self.output_root
                            / species
                            / f"{post_id}.{ext}"
                        )

                        metadata_path = (
                            self.metadata_root
                            / species
                            / f"{post_id}.json"
                        )

                        success = await download_file(
                            session,
                            image_url,
                            image_path,
                        )

                        if not success:
                            continue

                        try:
                            phash = Hashing.phash(image_path)
                        except Exception as e:
                            print(f"Hashing failed: {image_path} -> {e}")
                            continue
                        metadata = {
                            "id": post_id,
                            "species": species,
                            "source": "e621",
                            "image_path": str(image_path),
                            "url": image_url,
                            "tags": post.get("tags", {}),
                            "phash": phash,
                        }

                        MetadataWriter.save(metadata_path, metadata)

                        downloaded += 1

                        print(f"[{species}] {downloaded}")

                        if downloaded >= self.limit:
                            break

                page += 1
