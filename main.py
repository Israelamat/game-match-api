import pandas as pd
from fastapi import FastAPI
import uvicorn
import os
import requests
from utilities.formatter import format_games_dataframe 


app = FastAPI()

#Load dataset
dataset_local_path = "data/games.csv"
dataset_github_release_url = "https://github.com/Israelamat/game-match-api/releases/download/v1.0/games.csv"

os.makedirs("data", exist_ok=True)

if os.path.exists(dataset_local_path):
    print("CSV found in /data/, using it...")
else:
    print("CSV not found in /data/, downloading it from github...")
    r = requests.get(dataset_github_release_url)
    if r.status_code == 200:
        with open(dataset_local_path, "wb") as f: 
            f.write(r.content)
        print("CSV downloaded and saved in /data/")
    else:
        print("Error downloading CSV:", r.status_code)

try:
    df = pd.read_csv(dataset_local_path, nrows=1000, sep=",", quotechar='"', dtype=str, index_col=False)
    print("Data loaded")
except:
    df = pd.DataFrame()
    print("Data not loaded")

# Clean & format dataframe
df = format_games_dataframe(df)
print(df.columns)
print(df.head(2))

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