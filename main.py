import asyncio

from config import DOWNLOAD_ROOT
from config import E621_USER_AGENT
from config import MAX_IMAGES_PER_SPECIES
from config import METADATA_ROOT

from scrapers.e621_scraper import E621Scraper


async def load_species():
    with open("species.txt", "r", encoding="utf-8") as f:
        return [x.strip() for x in f if x.strip()]


async def main():
    species_list = await load_species()

    scraper = E621Scraper(
        user_agent=E621_USER_AGENT,
        output_root=DOWNLOAD_ROOT,
        metadata_root=METADATA_ROOT,
        limit=MAX_IMAGES_PER_SPECIES,
    )

    for species in species_list:
        print(f"Starting {species}")
        await scraper.scrape_species(species)


if __name__ == "__main__":
    asyncio.run(main())
