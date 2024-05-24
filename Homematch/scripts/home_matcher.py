import os
import sys
import asyncio
import json
from typing import List

from scripts.db_semantic_searcher import ListingSearcher
from scripts.listing_personalizer import ListingPersonalizer
from scripts.listings_creator_langchain import ListingsGenerator
from scripts.resources.consts import BUYER_PREFERENCES_STR

current_file_path = os.path.abspath(__file__)
project_root_path = os.path.dirname(os.path.dirname(current_file_path))

# Add the project root to the PYTHONPATH
sys.path.append(project_root_path)


class HomeMatcher:
    """
    The main module that coordinates the generation, searching, and personalization of home listings.
    """

    def __init__(self, api_key: str = os.getenv("OPENAI_API_KEY")):
        self.api_key = api_key
        self.listing_generator = ListingsGenerator()
        self.listing_searcher = ListingSearcher()
        self.listing_personalizer = ListingPersonalizer()

    async def match(self) -> List[dict]:
        await self.listing_generator.generate_listings()  # In reality would be an extraction from a database
        listing_similar_to_customer_preferences = self.listing_searcher.search_listings(BUYER_PREFERENCES_STR)
        personalized_listings = await self.listing_personalizer.personalize_listings(BUYER_PREFERENCES_STR,
                                                                                     listing_similar_to_customer_preferences)
        personalized_listings_json = [listing.dict() for listing in personalized_listings]
        listings_json_path = "resources/personalized_listings.json"
        with open(listings_json_path, "w") as f:
            json.dump(personalized_listings_json, f, indent=4)

        print(f"Personalized listings saved to {listings_json_path}")

    @staticmethod
    def load_matches() -> List[dict]:
        with open("resources/personalized_listings.json", "r") as f:
            matches = json.load(f)

        return matches


async def main():
    if len(sys.argv) != 2 and not os.getenv("OPENAI_API_KEY"):
        print(
            "Usage in CLI: 'python scripts/home_matcher.py OPENAI_API_KEY' or set OPENAI_API_KEY environment variable.")
        sys.exit(1)

    openai_api_key = sys.argv[1] if len(sys.argv) == 2 else os.getenv("OPENAI_API_KEY")
    home_matcher = HomeMatcher(api_key=openai_api_key)
    results = await home_matcher.match()
    print(results)


if __name__ == "__main__":
    # Run the main async function
    asyncio.run(main())
