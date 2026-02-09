import pandas as pd
from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

#Load dataset
dataset_path = "data/games.csv"

try:
    df = pd.read_csv("data/games.csv", nrows=1000)
    print("Data loaded")
except:
    df = pd.DataFrame()
    print("Data not loaded")

# Routes 
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/games")
async def games():
    if(df.empty):
        return {"message": "Dataset empty"}
    df_copy = df.copy().fillna("").head(5)
    df_native_types = df_copy.astype(object).to_dict(orient="records")
    return {
        "total": len(df_native_types),
        "games": df_native_types
    }

# Init app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)