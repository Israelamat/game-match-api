import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

df = pd.read_csv("../data/games_cleaned.csv",  keep_default_na=False)

mapping = {
    "AppID": "app_id",
    "Name": "title",
    "About the game": "description",
    "Price": "price",
    "Header image": "header_image",
    "Genres": "genres",
    "Tags": "tags",
    "Developers": "developer",
    "Screenshots": "screenshot",
    "metadata": "metadata"
}

df_db = df[list(mapping.keys())].rename(columns=mapping)

df_db['stock'] = 99
df_db['created_at'] = datetime.now() 
df_db['created_by_id'] = None 

print(f"Starting writing to the database of {len(df_db)} games...")
try:
    df_db.to_sql('game', con=engine, if_exists='append', index=False, chunksize=1000)
    print("Succesful")
except Exception as e:
    print(f"Sql error: {e}")