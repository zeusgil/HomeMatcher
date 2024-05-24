import asyncio
import json
from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain.schema import Document
from pydantic import ValidationError

from scripts.call_gen_ai_langchain import GenAICaller
from scripts.db_semantic_searcher import ListingSearcher
from scripts.models import HouseListing, ListingConverter, AugmentedDescription
from scripts.resources.consts import BUYER_PREFERENCES_STR, \
    BUYER_PERSONALIZATION_PROMPT, BUYER_PERSONALIZATION_SYSTEM_PROMPT, BUYER_PERSONALIZATION_FEW_SHOT_EXAMPLES


class ListingPersonalizer:
    """
    Description:
    A class to personalize property listings based on buyer preferences.

    LLM Augmentation:
    This process uses the LLM to augment the description of each retrieved listing,
    tailoring it to resonate with the buyer’s specific preferences. The goal is to
    subtly emphasize aspects of the property that align with what the buyer is looking for.

    Maintaining Factual Integrity:
    The augmentation process is designed to enhance the appeal of the listing
    without altering any factual information.

    Phases:
    1. It then retrieves the top listings that match the buyer’s preferences from db_semantic_searcher.py.
    2. For each listing, it augments the description using the LLM.

    """

    def __init__(self, db_path="resources/listings.db"):
        self.listing_searcher = ListingSearcher(db_path=db_path)
        self.gen_ai_caller = GenAICaller()
        self.listing_converter = ListingConverter()

    async def personalize_listings(self, buyer_preferences: str, listings: List[Document]) -> List[HouseListing]:
        listings = [self.listing_converter.convert_text_to_houselisting(listing) for listing in listings]
        print("Creating personalized listings...")
        for listing in listings:
            buyer_personalization_prompt = BUYER_PERSONALIZATION_PROMPT.format(buyer_preferences=buyer_preferences,
                                                                               listing_description=listing.description)
            augmented_description = await self.gen_ai_caller.call_gen_ai(
                system_prompt=BUYER_PERSONALIZATION_SYSTEM_PROMPT,
                prompt=buyer_personalization_prompt,
                few_shot_examples=BUYER_PERSONALIZATION_FEW_SHOT_EXAMPLES,
                parser=PydanticOutputParser(pydantic_object=AugmentedDescription)
            )
            augmented_description, max_retries, retries = await self._retry_call_until_success(augmented_description,
                                                                                               buyer_personalization_prompt)

            if retries >= max_retries:
                print("Max retries reached, proceeding without augmented description")
                listing.augmented_description = listing.description

            else:
                listing.augmented_description = augmented_description.get("Augmented Description", "")

        return listings

    async def _retry_call_until_success(self, augmented_description, buyer_personalization_prompt):
        augmented_description = None
        retries = 0
        max_retries = 5
        while (
                augmented_description is None or "Augmented Description" not in augmented_description) and retries < max_retries:
            try:
                augmented_description = await self.gen_ai_caller.call_gen_ai(
                    system_prompt=BUYER_PERSONALIZATION_SYSTEM_PROMPT,
                    prompt=buyer_personalization_prompt,
                    few_shot_examples=BUYER_PERSONALIZATION_FEW_SHOT_EXAMPLES,
                    parser=PydanticOutputParser(pydantic_object=AugmentedDescription)
                )
            except ValidationError as e:
                print(f"Error parsing response: {e}")

            except Exception as e:
                print(f"Unexpected error: {e}")

            retries += 1

            # Sleep for a short period before retrying to avoid too many rapid retries
            await asyncio.sleep(1)

        return augmented_description, max_retries, retries


if __name__ == "__main__":
    listing_personalizer = ListingPersonalizer()
    listing_searcher = ListingSearcher()
    listings = listing_searcher.search_listings(BUYER_PREFERENCES_STR)
    personalized_listings = asyncio.run(listing_personalizer.personalize_listings(BUYER_PREFERENCES_STR, listings))
    personalized_listings_json = [listing.dict() for listing in personalized_listings]
    with open("resources/personalized_listings.json", "w") as f:
        json.dump(personalized_listings_json, f, indent=4)
