# 🎮 Steam Game Recommender API

Steam Game Recommender is a **content-based recommendation system** built with Python and FastAPI.  
It analyzes Steam games and returns similar titles based on their attributes such as genres, tags, developers, and publishers.

The system uses **TF-IDF vectorization** combined with **cosine similarity** to generate meaningful recommendations.

---

## 🚀 Features

- 📊 Data preprocessing and cleaning of Steam dataset
- 🧹 Handling missing and inconsistent values
  - Normalization of release dates
  - Conversion of numeric fields (int/float)
  - Boolean standardization (Windows / Mac / Linux support)
  - Missing value handling
- 🎮 Content-based recommendation engine
  - Uses game metadata (genres, tags, developers, publishers)
  - Finds similarity between games
- 🧠 TF-IDF vectorization for feature extraction
- 📐 Cosine similarity for recommendation ranking
- ⚡ FastAPI REST API for real-time queries
- 💾 Pickle-based model persistence for faster startup

---

## 📦 Installation

Clone the repository:

````Bash
git clone <repo-url>
````
Create virtual environment:


````Bash
python -m venv venv
````
Activate environment:

Windows:
````Bash
venv\Scripts\activate
````
Install dependencies:
````Bash
pip install -r requirements.txt
````
---

## ▶️ Run the API

Start the FastAPI server:
````Bash
uvicorn main:app --reload
````
Then open:

http://127.0.0.1:8000/docs

---

## 🧠 How Recommendations Work (TF-IDF)

The system converts game metadata into numerical vectors using **TF-IDF (Term Frequency - Inverse Document Frequency)**.

### 📌 TF-IDF Formula

TF-IDF is calculated as:

![TF-IDF and Cosine Similarity](img/TF-IDF%20and%20cosine%20similarity.png)

Where:

- TF(t, d) = frequency of term *t* in document *d*
- DF(t) = number of documents containing term *t*
- N = total number of documents

---

### 📊 Intuition

- Words that appear frequently in a game description are important (TF)
- Words that appear in many games are less useful (DF penalty)
- Final score highlights **unique and relevant features per game**

---

### 🎯 Recommendation Process

1. Each game is transformed into a TF-IDF vector
2. Cosine similarity is computed between vectors

Cosine similarity:

similarity = (A · B) / (||A|| × ||B||)

:contentReference[oaicite:0]{index=0}

3. Games with highest similarity scores are returned

---

## 📈 Output

The API returns a JSON list of the most similar games:

- Game title
- Similarity score
