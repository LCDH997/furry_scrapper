from abc import ABC, abstractmethod


class BaseScraper(ABC):
    @abstractmethod
    async def scrape_species(self, species: str):
        pass
