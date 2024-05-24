# Home Matcher

This repository contains modules for generating, searching, and personalizing home listings based on buyer preferences. The main entry point is the `home_matcher.py` script, which orchestrates the entire process.

jupyter notebook in scripts/home_matcher.ipynb
If you wish to run this repository using Jupyter Notebook, please refer to the following link: [Home Matcher](scripts/home_matcher.ipynb)

## Modules

### 1. Home Matcher (`scripts/home_matcher.py`)

**Description:**
The main module that coordinates the generation, searching, and personalization of home listings.

**Classes and Public Functions:**
- `HomeMatcher`
  - `__init__(self)`: Initializes the necessary components.
  - `match(self)`: Runs the entire matching process, generating listings, searching based on buyer preferences, and personalizing the results.

**Input Files:**
- None (Listings are generated or extracted from a database).

**Output Files:**
- `resources/personalized_listings.json`: Stores the personalized listings in JSON format.

Run the main module:

#Use sys to add the path to the scripts folder
```bash
python scripts/home_matcher.py OPENAI_API_KEY 
```

### 2. Listings Generator (`scripts/listings_creator_langchain.py`)

**Description:**
Generates home listings using a language model and stores them in a database.

**Classes and Public Functions:**
- `ListingsGenerator`
  - `__init__(self, db_path="resources/listings.db")`: Initializes the generator with the specified database path.
  - `generate_listings(self)`: Generates listings and saves them to a JSON file and a database.
  - `store_listings_in_db(self, gen_ai_response: List[HouseListing])`: Stores the generated listings in a ChromaDB database.

**Input Files:**
- Prompts and few-shot examples for generating listings.

**Output Files:**
- `resources/listings.json`: Stores the generated listings in JSON format.
- `resources/listings.db`: The database where listings are stored as embeddings.

### 3. Listing Searcher (`scripts/db_semantic_searcher.py`)

**Description:**
Performs a semantic search on the home listings database to find listings similar to a given query.

**Classes and Public Functions:**
- `ListingSearcher`
  - `__init__(self, db_path="resources/listings.db")`: Initializes the searcher with the specified database path.
  - `search_listings(self, query: str)`: Searches the database for listings similar to the query.

**Input Files:**
- `resources/listings.db`: The database containing listings embeddings.

**Output Files:**
- None (Results are returned directly).

### 4. Listing Personalizer (`scripts/listing_personalizer.py`)

**Description:**
Personalizes property listings based on buyer preferences using a language model to augment the description of each listing.

**Classes and Public Functions:**
- `ListingPersonalizer`
  - `__init__(self, db_path="resources/listings.db")`: Initializes the personalizer with the specified database path.
  - `personalize_listings(self, buyer_preferences: str, listings: List[Document])`: Personalizes listings based on buyer preferences.

**Input Files:**
- Buyer preferences as a string.
- Listings retrieved from the database.

**Output Files:**
- Personalized listings returned directly.

### 5. Gen AI Caller (`scripts/call_gen_ai_langchain.py`)

**Description:**
Handles calls to the language model API for generating and personalizing listings.

**Classes and Public Functions:**
- `GenAICaller`
  - `__init__(self)`: Initializes the Gen AI caller.
  - `call_gen_ai(self, system_prompt: str, prompt: str, few_shot_examples: str = None, parser: PydanticOutputParser = None)`: Calls the language model API.
  - `get_gen_ai_response(self, system_prompt, user_prompt: str, few_shot_examples: str = None, parser: PydanticOutputParser = None)`: Internal method to get a response from the language model.
  - `create_query(self, few_shot_examples: str, parser: PydanticOutputParser, system_prompt: str, user_prompt: str)`: Creates a query for the language model.
  - `safe_json_loads(self, response: str)`: Safely loads a JSON response.
  - `correct_json_parsing(self, score: str)`: Corrects JSON parsing issues.

**Input Files:**
- Prompts and few-shot examples for generating and personalizing listings.

**Output Files:**
- None (Results are returned directly).

### 6. Models (`scripts/models.py`)

**Description:**
Contains data models used throughout the modules.

**Classes and Public Functions:**
- `HouseListing`: Data model for a house listing.
- `AugmentedDescription`: Data model for an augmented description.
- `ListingConverter`: Utility class for converting between text and `HouseListing` objects.
  - `convert_houselisting_to_text(self, listing: HouseListing)`: Converts a `HouseListing` object to text.
  - `convert_text_to_houselisting(self, listing_text: Document)`: Converts text to a `HouseListing` object.

**Input Files:**
- None (Used internally within other modules).

**Output Files:**
- None (Used internally within other modules).

## Utils and Constants

### Utils (`scripts/utils/utils.py`)

**Description:**
Contains utility functions.

**Files:**
- `utils.py`: Contains various utility functions.

**Input Files:**
- None (Used internally within other modules).

**Output Files:**
- None (Used internally within other modules).

### Constants (`scripts/resources/consts.py`)

**Description:**
Contains constant values used throughout the modules.

**Files:**
- `consts.py`: Defines constant values.

**Input Files:**
- None (Used internally within other modules).

**Output Files:**
- None (Used internally within other modules).

## Directory Structure

./
scripts/
listings_creator_langchain.py
call_gen_ai_langchain.py
models.py
resources/
personalized_listings.json
init.py
consts.py
listings.db/
chroma.sqlite3
listings.json
listing_personalizer.py
home_matcher.py
db_semantic_searcher.py
call_gen_ai.py
Pipfile
Pipfile.lock


## How to Run

1. Ensure you have all dependencies installed by running `pipenv install`.
```bash
pipenv shell
```
```bash
pipenv install
```
or (if you don't have pipenv installed)
```bash
pipenv sync
```
2. Set up your OpenAI API key as an environment variable `OPENAI_API_KEY` to run directly or use CLI like in step 3.
3. Run the main module:

```bash
python scripts/home_matcher.py OPENAI_API_KEY 
```
