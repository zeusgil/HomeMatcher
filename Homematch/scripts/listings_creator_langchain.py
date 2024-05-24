import asyncio
import json
import os
from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

from scripts.call_gen_ai_langchain import GenAICaller
from scripts.models import HouseListing, ListingConverter
from scripts.resources.consts import LISTINGS_SYSTEM_PROMPT, LISTINGS_PROMPT_QUESTION, LISTINGS_FEW_SHOT_EXAMPLE


class ListingsGenerator:
    def __init__(self, db_path="resources/listings.db"):
        self.db_path = db_path
        self.gen_ai_caller = GenAICaller()
        self.listing_converter = ListingConverter()

    async def generate_listings(self) -> None:
        print("Generating listings...")
        gen_ai_response = await self.gen_ai_caller.call_gen_ai(LISTINGS_SYSTEM_PROMPT, LISTINGS_PROMPT_QUESTION,
                                                               LISTINGS_FEW_SHOT_EXAMPLE,
                                                               parser=PydanticOutputParser(pydantic_object=HouseListing)
                                                               )
        print(f"Saving listings to resources/listings.json")
        # Convert each listing into HouseListing object:
        with open("resources/listings.json", "w") as f:
            json.dump(gen_ai_response, f, indent=4)

        gen_ai_response_formatted = [HouseListing(**listing) if listing else None for listing in
                                     gen_ai_response.values()]
        gen_ai_response_formatted = [listing for listing in gen_ai_response_formatted if listing]
        await self.store_listings_in_db(gen_ai_response_formatted)

    async def store_listings_in_db(self, gen_ai_response: List[HouseListing]) -> None:
        embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        listings_texts = [self.listing_converter.convert_houselisting_to_text(listing) for listing in gen_ai_response]
        text_splitter = CharacterTextSplitter(
            separator="Listing",
            chunk_size=1000,
            chunk_overlap=0,
            length_function=len,
            is_separator_regex=False
        )
        docs = text_splitter.create_documents(listings_texts)
        db = Chroma.from_documents(docs, embeddings, persist_directory=self.db_path,
                                   collection_name="listings_embeddings")
        print(f"Listings are stored in ChromaDB path: {self.db_path}")
        print(f"Count of items in db: {db._collection.count()}")
        # save db to local disk
        db.persist()
        print(f"Listings stored in ChromaDB")

    @staticmethod
    def load_listings() -> List[HouseListing]:
        with open("resources/listings.json", "r") as f:
            listings = json.load(f)

        return listings


if __name__ == "__main__":
    listings_generator = ListingsGenerator()
    asyncio.run(listings_generator.generate_listings())
