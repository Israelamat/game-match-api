# Steam Game Recommender API

A simple content-based game recommendation system for Steam games. Input a game name and get 4–5 similar games based on genres, tags, developers, and other attributes.

---

## Features

- **CSV Data Cleaning**
  - Replace `"0 - 0"` release dates with empty strings
  - Convert numeric fields from strings to integers/floats
  - Ensure boolean fields (`Windows`, `Mac`, `Linux`) are proper True/False values
  - Fill missing values with empty strings

- **Content-Based Game Recommendations**
  - Recommends games based on similarity of genres, tags, developers, publishers, and other attributes
  - Uses TF-IDF vectorization and cosine similarity

- **FastAPI Integration**
  - Query with a game name to get similar games as JSON

- **Pickle Support**
  - Pre-saved vectorizer and cleaned DataFrame for faster API startup

---

## Installation

1. Clone the repository environment::
2. Create a virtual :
`python -m venv venv`
`venv\Scripts\activate`
3. Install dependencies:
`pip install -r requirements.txt`
   

