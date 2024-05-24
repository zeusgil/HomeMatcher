from typing import Optional
import re

from langchain.schema import Document
from pydantic import Field, BaseModel
from pydantic.v1 import validator


class HouseListing(BaseModel):
    neighborhood: str = Field(..., alias="Neighborhood")
    price: str = Field(..., alias="Price", description="Price in dollars")
    bedrooms: float = Field(..., alias="Bedrooms")
    bathrooms: float = Field(..., alias="Bathrooms")
    house_size: str = Field(..., alias="House Size", description="House size in square feet")
    description: str = Field(..., alias="Description", description="Description of the house")
    augmented_description: Optional[str] = Field(None,
                                                 alias="Augmented Description",
                                                 description="Augmented description of the house")

    @validator('price')
    def price_must_be_positive_numeric(cls, value):
        val = value[1:]
        if val <= 0:
            raise ValueError('Price must be a positive integer')

        if not val.isnumeric():
            raise ValueError('Price must be a numeric value')

        return value

    @validator('price')
    def price_must_start_with_dollar_sign(cls, value):
        if not str(value).startswith('$'):
            raise ValueError('Price must start with "$"')

        return value

    @validator('bedrooms', 'bathrooms')
    def number_of_rooms_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError('Number of rooms must be a positive integer')

        return value

    @validator('house_size')
    def house_size_must_be_valid_format(cls, value):
        if not value.endswith('sqft'):
            raise ValueError('House size must end with "sqft"')

        return value

    @validator('house_size')
    def house_size_must_be_positive_numeric(cls, value):
        val = value[:-4]
        if not val.isnumeric():
            raise ValueError('House size must be a numeric value followed by "sqft"')

        if not int(val) > 0:
            raise ValueError('House size must be a positive integer')

        return value

    @validator('description')
    def has_house_description(cls, value):
        if not value:
            raise ValueError('Description must not be empty')

        return value


class AugmentedDescription(BaseModel):
    augmented_description: Optional[str] = Field(None,
                                                 alias="Augmented Description",
                                                 description="Augmented description of the house")


class ListingConverter:

    @staticmethod
    def convert_houselisting_to_text(listing: HouseListing) -> str:
        return (f"neighborhood:{listing.neighborhood}\n"
                f"price:{listing.price}\n"
                f"bedrooms:{listing.bedrooms}\n"
                f"bathrooms:{listing.bathrooms}\n"
                f"house size:{listing.house_size}\n"
                f"description:{listing.description}")

    @staticmethod
    def convert_text_to_houselisting(listing_text: Document) -> HouseListing:
        parsed_data = {}
        patterns = {
            'Neighborhood': re.compile(r'neighborhood:(.*?)\n'),
            'Price': re.compile(r'price:(.*?)\n'),
            'Bedrooms': re.compile(r'bedrooms:(.*?)\n'),
            'Bathrooms': re.compile(r'bathrooms:(.*?)\n'),
            'House Size': re.compile(r'house size:(.*?)\n'),
            'Description': re.compile(r'description:(.*)', re.DOTALL)
        }

        for key, pattern in patterns.items():
            match = pattern.search(listing_text.page_content)
            if match:
                parsed_data[key] = match.group(1).strip()

        return HouseListing(**parsed_data)
