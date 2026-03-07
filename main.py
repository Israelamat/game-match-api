import pandas as pd
from fastapi import FastAPI
import uvicorn
import os
import csv
from utilities.formatter import format_games_dataframe
from utilities.dataframe_cleanner import clean_dataframe
from utilities.data_manager import ensure_dataset_exists
from recommender.recommender import GameRecommender
from dotenv import load_dotenv
from pathlib import Path 
app = FastAPI()

#Load dataset
load_dotenv()
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

DATASET_LOCAL_PATH = os.getenv("DATASET_LOCAL_PATH")
DATASET_CLEANED_PATH = os.getenv("DATASET_CLEANED_PATH")
DATASET_GITHUB_URL = os.getenv("DATASET_GITHUB_URL")


ensure_dataset_exists(DATASET_LOCAL_PATH, DATASET_GITHUB_URL)

if os.path.exists(DATASET_CLEANED_PATH):
    print(f"Found cleaned dataset at {DATASET_CLEANED_PATH}. Loading...")
    df = pd.read_csv(DATASET_CLEANED_PATH, keep_default_na=False)
    print(f"Data loaded from cache. Total games: {len(df)}")
    #df = df.head(10)
else:
    print("Clean dataset not found. Starting cleaning process...")
    try:
        df_raw = pd.read_csv(DATASET_LOCAL_PATH, sep=",", quotechar='"', dtype=str, index_col=False)
        df = format_games_dataframe(df_raw)
        df = clean_dataframe(df)
        
        print("Data formatting and cleaning completed")
        df.to_csv(DATASET_CLEANED_PATH, index=False, quoting=csv.QUOTE_ALL, sep=",")
        print(f"Data saved in: {DATASET_CLEANED_PATH}")
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
        "results": len(df_native_types) ,
    }

recommender = GameRecommender(df)

if not recommender.load_model():
    recommender.fit()
    recommender.save_model()

@app.get("/recommend/{game_name}")
async def get_rec(game_name: str):
    results = recommender.get_recommendations(game_name)
    return {"results": results}

@app.get("recomend/{game_id}")
async def get_rec(game_id: int):
    results = recommender.get_recommendations(game_id)
    return {"results": results}

# Init app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)