import pandas as pd
from fastapi import FastAPI
import uvicorn
import os
import csv
from utilities.formatter import format_games_dataframe
from utilities.dataframe_cleanner import clean_dataframe
from utilities.data_manager import ensure_dataset_exists
from recommender.recommender import GameRecommender

app = FastAPI()

#Load dataset
dataset_local_path = "data/games.csv"
cleaned_path = "data/games_cleaned.csv"
dataset_github_release_url = "https://github.com/Israelamat/game-match-api/releases/download/v1.0/games.csv"

ensure_dataset_exists(dataset_local_path, dataset_github_release_url)

if os.path.exists(cleaned_path):
    print(f"Found cleaned dataset at {cleaned_path}. Loading...")
    df = pd.read_csv(cleaned_path, keep_default_na=False)
    print(f"Data loaded from cache. Total games: {len(df)}")
    #df = df.head(10)
else:
    print("Clean dataset not found. Starting cleaning process...")
    try:
        df_raw = pd.read_csv(dataset_local_path, sep=",", quotechar='"', dtype=str, index_col=False)
        df = format_games_dataframe(df_raw)
        df = clean_dataframe(df)
        
        print("Data formatting and cleaning completed")
        df.to_csv(cleaned_path, index=False, quoting=csv.QUOTE_ALL, sep=",")
        print(f"Data saved in: {cleaned_path}")
        #df = df.head(10)

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
        "total": len(df_native_types),
        "results": df_native_types,
    }

recommender = GameRecommender(df)

if not recommender.load_model():
    recommender.fit()
    recommender.save_model()

@app.get("/recommend/{game_name}")
async def get_rec(game_name: str):
    results = recommender.get_recommendations(game_name)
    return {"results": results}

# Init app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)