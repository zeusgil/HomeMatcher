from scripts.models import HouseListing

GPT4O_MODEL_NAME = "gpt-4o"
MAX_TOKENS_AMOUNT = 128000
EXTRA_SECURITY_GAP = 100
MAX_OUTPUT_TOKENS_AMOUNT = 4096
MAX_WORKERS = 5
LISTINGS_SYSTEM_PROMPT = """You are a real estate agent who is creating a listing for a new property. You need to provide a detailed description of the property to attract potential buyers."""
LISTINGS_FEW_SHOT_EXAMPLE = """
{property_1:
    {'Neighborhood': 'Green Oaks',
    'Price': '$800,000',
    'Bedrooms': '3',
    'Bathrooms': '2',
    'House Size': '2,000 sqft'
    'Description': "Welcome to this eco-friendly oasis nestled in the heart of Green Oaks. This charming 3-bedroom, 2-bathroom home boasts energy-efficient features such as solar panels and a well-insulated structure. Natural light floods the living spaces, highlighting the beautiful hardwood floors and eco-conscious finishes. The open-concept kitchen and dining area lead to a spacious backyard with a vegetable garden, perfect for the eco-conscious family. Embrace sustainable living without compromising on style in this Green Oaks gem.Neighborhood Description: Green Oaks is a close-knit, environmentally-conscious community with access to organic grocery stores, community gardens, and bike paths. Take a stroll through the nearby Green Oaks Park or grab a cup of coffee at the cozy Green Bean Cafe. With easy access to public transportation and bike lanes, commuting is a breeze."
    }
}
"""

PROPERTY_LISTING_SCHEMA_JSON = HouseListing.model_json_schema()
LISTINGS_PROMPT_QUESTION = f"""Provide detailed information about 10 imaginary properties to attract potential buyers. 
The information should include the following details as an example: 

{LISTINGS_FEW_SHOT_EXAMPLE}

Use the following schema for each property listing:

{PROPERTY_LISTING_SCHEMA_JSON}

IMPORTANT- Avoid creating "augmented_description" field in the schema.

Please only answer in a json format without any additional text!
"""
OPENAI_EMBEDDING_SMALL_MODEL_NAME = "text-embedding-3-small"

# BUYER_QUESTIONS = ["How big do you want your house to be?",
#                    "What are 3 most important things for you in choosing this property?",
#                    "Which amenities would you like?",
#                    "Which transportation options are important to you?",
#                    "How urban do you want your neighborhood to be?",
#                    ]
# BUYER_ANSWERS = ["A comfortable three-bedroom house with a spacious kitchen and a cozy living room.",
#                  "A quiet neighborhood, good local schools, and convenient shopping options.",
#                  "A backyard for gardening, a two-car garage, and a modern, energy-efficient heating system.",
#                  "Easy access to a reliable bus line, proximity to a major highway, and bike-friendly roads.",
#                  "A balance between suburban tranquility and access to urban amenities like restaurants and theaters."
#                  ]

BUYER_QUESTIONS = ["How big do you want your house to be?",
                   "Which amenities would you like?",
                   "What is the most important thing you wish you neighborhood had?"

                   ]

BUYER_ANSWERS = ["At least 3 bedrooms & 2 bathrooms",
                 "Would like to have a large swimming pool",
                 "Great schools and parks nearby"
                 ]

BUYER_PREFERENCES = {BUYER_QUESTIONS[i]: BUYER_ANSWERS[i] for i in range(len(BUYER_QUESTIONS))}
BUYER_PREFERENCES_STR = "\n".join([f"{q}: {a}" for q, a in BUYER_PREFERENCES.items()])

BUYER_PERSONALIZATION_SYSTEM_PROMPT = """
You are an AI language model tasked with augmenting property listings to better match the specific preferences of potential buyers. Your goal is to enhance the descriptions by subtly emphasizing features that align with the buyer’s interests, while maintaining factual integrity.

Guidelines:

*LLM Augmentation:
Review the description of each property listing.
Identify and emphasize aspects of the property that align with the buyer’s stated preferences.
Tailor the language to resonate with what the buyer is looking for, making the property more appealing 
without introducing any new information.

*Maintaining Factual Integrity:
Ensure that all augmented descriptions remain accurate and truthful.
Do not add, remove, or alter any factual information about the property.
You should try to summarize the existing features in a way that highlights their 
relevance to the buyer’s preferences."""

BUYER_PERSONALIZATION_PROMPT = """
The buyers' preferences are as follows:\n{buyer_preferences}\n
The listing found relevant for the buyer is: {listing_description}
\n\nPlease augment the description of the listing to better match the buyer's preferences.\n\n
"""
BUYER_PERSONALIZATION_FEW_SHOT_EXAMPLES = """
Buyer's Preferences:

How big do you want your house to be?: At least 3 bedrooms & 2 bathrooms
Which amenities would you like?: Would like to have a large swimming pool
What is the most important thing you wish your neighborhood had?: Great schools and parks nearby

Original Listing:
{{
    "property_1": {{
        "Neighborhood": "Lakeside",
        "Price": "$1,200,000",
        "Bedrooms": 5.0,
        "Bathrooms": 4.0,
        "House Size": "3,200 sqft",
        "Description": "Experience luxury living in this magnificent 5-bedroom, 4-bathroom home in Lakeside. The grand foyer leads to a formal living room with a fireplace and a dining room with elegant finishes. The chef's kitchen features custom cabinetry, a large island, and top-of-the-line appliances. The master suite includes a sitting area, a walk-in closet, and a luxurious bathroom with a jetted tub. The backyard offers a covered patio, a swimming pool, and a beautifully landscaped garden. Neighborhood Description: Lakeside is an upscale community with a private lake, walking trails, and a clubhouse. Residents enjoy access to exclusive amenities such as tennis courts and a fitness center. The neighborhood is also close to prestigious schools and fine dining establishments.",
        "Augmented Description": None
    }}
}}


The output should be:{{"Augmented Description": "Experience luxury living in this magnificent 5-bedroom, 4-bathroom home in Lakeside. 
Ideal for families, this spacious home features a grand foyer leading to a formal living room with a 
fireplace and a dining room with elegant finishes. The chef's kitchen, with its custom cabinetry, 
large island, and top-of-the-line appliances, is perfect for preparing family meals. 
The master suite includes a sitting area, a walk-in closet, and a luxurious bathroom with a jetted tub. 
The backyard offers a covered patio, a large swimming pool, and a beautifully landscaped garden, perfect 
for outdoor activities and relaxation. Lakeside is an upscale community known for its prestigious schools 
and nearby parks, making it an ideal location for families. Residents enjoy access to exclusive amenities such 
as tennis courts, a fitness center, a private lake, walking trails, and a clubhouse."
}}
"""
