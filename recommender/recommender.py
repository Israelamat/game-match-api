import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pickle
import os

class GameRecommender:
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the GameRecommender class.
        Metadata is a combination of text columns for Tf-IDF vectorization.
        """
        self.df = df.reset_index(drop=True)
        self.df = df.fillna("").reset_index(drop=True)
        
        # Limit the number of features to 5000 for faster processing do not kill the RAM
        stopwords = [
            'singleplayer', 'multiplayer', 'coop', 'online', 'steam', 'achievements', 
            'controller', 'support', 'full', 'cards', 'trading', 'cloud', 'family', 
            'sharing', 'camera', 'comfort', 'volume', 'controls', 'playable', 'timed', 
            'input', 'save', 'anytime', 'stereo', 'sound', 'surround', 'remote', 'play', 
            'phone', 'tablet', 'tv', 'together', 'captions', 'available', 'stats', 
            'includes', 'editor', 'commentary', 'crossplatform', 'adjustable', 'difficulty'
        ]
        self.vectorizer = TfidfVectorizer(
            stop_words=stopwords, 
            max_features=50000,  
            min_df=2,
            ngram_range=(1, 2)  
        )
        self.tfidf_matrix = None

    def fit(self):
        """Fit the TF-IDF vectorizer and calculate the TF-IDF matrix."""
        print("Fitting the model with 114.000 games...")
        # Llenamos vacíos por seguridad y transformamos
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['metadata'].fillna(''))
        print("Model fitted")
        
    def save_model(self, path="data/model_data.pkl"):
        """Save the vectorizer and TF-IDF matrix to a file."""
        with open(path, "wb") as f:
            pickle.dump((self.vectorizer, self.tfidf_matrix), f)
        print(f"Model saved to {path}")

    def load_model(self, path="data/model_data.pkl"):
        """Load the vectorizer and TF-IDF matrix from a file."""
        if os.path.exists(path):
            with open(path, "rb") as f:
                self.vectorizer, self.tfidf_matrix = pickle.load(f)
            print(f"Model loaded from {path}")
            return True
        return False

    def get_recommendations(self, game_name: str, n: int = 5):
        """
        Get recommendations for a specific game.
        :param game_name: The name of the game to get recommendations for.
        :param n: The number of recommendations to return.
        """
        # Get the index of the game
        game_name = game_name.strip().lower()
        idx_list = self.df.index[self.df['Name'].str.lower() == game_name.lower()].tolist()
        print(f"Input game {game_name}")
        
        if not idx_list:
            return None
        
        # Get the cosine similarity between the game and all other games
        idx = idx_list[0]
        cosine_sim = linear_kernel(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()
        related_indices = cosine_sim.argsort()[-(n+1):-1][::-1]
                
        # Build the response
        recommendations = []
        for i in related_indices:
            name = str(self.df.iloc[i]['Name'])
            app_id = str(self.df.iloc[i]['AppID'])
            tags = str(self.df.iloc[i].get('Tags', 'None'))
            genres = str(self.df.iloc[i].get('Genres', 'None'))
            image_url = f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/header.jpg" if app_id != "0" else None
            
            recommendations.append({
                "name": name if name != "nan" else "Unknown",
                "app_id": app_id if app_id != "nan" else "0",
                "image": image_url,
                "genres": genres if "Single-player" not in genres else tags, # Si genres es técnico, usa tags
                "similarity": f"{round(cosine_sim[i] * 100, 2)}%"
            })
            
        return recommendations