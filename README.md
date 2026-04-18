# 🎮 Steam Game Recommender API

Steam Game Recommender is a **content-based recommendation system** built with Python and FastAPI.  
It analyzes Steam games and returns similar titles based on their attributes such as genres, tags, developers, and publishers.

The system uses **TF-IDF vectorization** combined with **cosine similarity** to generate meaningful recommendations.

---
## ⚡ Automated Lifecycle & Pipeline

The core of this project is its **self-configuring pipeline**. Upon startup, the system detects the environment and executes the following flow:

1. **Auto-Data Acquisition**: If the `.csv` or `.pkl` files are missing, the system automatically fetches the raw dataset.
2. **Preprocessing & Cleaning**: 
   - Normalizes release dates and standardizes boolean platforms (Win/Mac/Linux).
   - Handles missing values and inconsistent numeric types.
3. **Model Training**: 
   - Vectorizes metadata using **TF-IDF**.
   - Computes the **Cosine Similarity** matrix.
4. **Persistence (Pickle)**: Saves the trained model to `.pkl` for near-instant API startup in subsequent runs.
5. **Database Export (ETL)**: Uses **SQLAlchemy** to dump the cleaned, processed data into a **MySQL** database (XAMPP/phpMyAdmin), making it available for external queries or reporting.
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
