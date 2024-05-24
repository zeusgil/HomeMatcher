import os
from typing import List

import chromadb
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores import Chroma

from scripts.resources.consts import BUYER_PREFERENCES_STR


class ListingSearcher:
    """
    Create a class that goes to listings.db chroma.sqlite database and performs a semantic search on the listings.
    The class should have a method that takes a query and returns the top 5 listings that are most similar to the query.
    """

    def __init__(self, db_path="resources/listings.db"):
        self.db_path = db_path
        self.chroma_client = chromadb.config.Settings(
            persist_directory=self.db_path,
        )

    def search_listings(self, query: str) -> List[Document]:
        print("Searching for similar listing")
        # load the existing db:
        db = self._load_chroma_db()
        most_similar = db.similarity_search(query, k=5)
        return most_similar

    def _load_chroma_db(self) -> Chroma:
        embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

        vectorstore = Chroma(
            collection_name="listings_embeddings",
            embedding_function=embeddings,
            persist_directory=self.db_path,
        )
        print(f"Count of items in db: {vectorstore._collection.count()}")
        return vectorstore


if __name__ == "__main__":
    listing_searcher = ListingSearcher()
    listing_searcher.search_listings(BUYER_PREFERENCES_STR)
