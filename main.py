import pandas as pd
from fastapi import FastAPI
import uvicorn
from utilities.formatter import format_games_dataframe
from utilities.dataframe_cleanner import clean_dataframe
from utilities.data_manager import ensure_dataset_exists
from recommender.recommender import GameRecommender

app = FastAPI()

#Load dataset
dataset_local_path = "data/games.csv"
dataset_github_release_url = "https://github.com/Israelamat/game-match-api/releases/download/v1.0/games.csv"

ensure_dataset_exists(dataset_local_path, dataset_github_release_url)

try:
    df_raw = pd.read_csv(dataset_local_path, sep=",", quotechar='"', dtype=str)
    df = format_games_dataframe(df_raw)
    df = clean_dataframe(df)
    print("Data formatting and cleaning completed")
    cleaned_path = "data/games_cleaned.csv"
    df.to_csv(cleaned_path, index=False)
    print(f"Data saved in: {cleaned_path}")

except Exception as e:
    df = pd.DataFrame()
    print(f"Error loading/cleaning data: {e}")

# Routes 
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/games")
async def games():
    if(df.empty):
        return {"message": "Dataset empty"}
    df_native_types = df.astype(object).to_dict(orient="records")
    return {
        "total": len(df_native_types)
    }

recommender = GameRecommender(df)

if not recommender.load_model():
    recommender.fit()
    recommender.save_model()

# Ruta de la API
@app.get("/recommend/{game_name}")
async def get_rec(game_name: str):
    results = recommender.get_recommendations(game_name)
    return {"results": results}

# Init app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)