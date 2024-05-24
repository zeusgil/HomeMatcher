import asyncio
import json
from typing import List

import chromadb

from scripts.call_gen_ai import GenAICaller
from scripts.models import HouseListing
from scripts.resources.consts import LISTINGS_SYSTEM_PROMPT, LISTINGS_PROMPT_QUESTION


class ListingsGenerator:
    def __init__(self, db_path="resources/listings.db"):
        self.gen_ai_caller = GenAICaller()
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        self.collection = self.chroma_client.create_collection("listings_embeddings")

    async def generate_listings(self):
        gen_ai_response = await self.gen_ai_caller.call_gen_ai(LISTINGS_SYSTEM_PROMPT, LISTINGS_PROMPT_QUESTION)
        print(f"Saving listings to resources/listings.json")
        # Convert each listing into HouseListing object:
        with open("resources/listings.json", "w") as f:
            json.dump(gen_ai_response, f, indent=4)

        gen_ai_response_formatted = [HouseListing(**listing) for listing in gen_ai_response.values()]
        await self.store_listings_in_db(gen_ai_response_formatted)

    async def store_listings_in_db(self, gen_ai_response: List[HouseListing]):
        embeddable_listings = []
        for index, listing in enumerate(gen_ai_response):
            temp_embedding = await self.gen_ai_caller.convert_to_embedding(listing)
            embeddable_listings.append(temp_embedding)
            self.collection.add(ids=str(index), embeddings=temp_embedding)

        print(f"Listings stored in ChromaDB")

    # async def fetch_listings_from_db(self) -> list:
    #     print("Fetching listings from ChromaDB")
    #     ids = self.collection.list_ids()
    #     listings = []
    #     for id in ids:
    #         listing = self.collection.get(id)
    #         listings.append(listing)
    #
    #     return listings


if __name__ == "__main__":
    listings_generator = ListingsGenerator()
    asyncio.run(listings_generator.generate_listings())
