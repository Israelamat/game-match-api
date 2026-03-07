import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

# Load the CSV
df = pd.read_csv("../data/games_cleaned.csv", keep_default_na=False)
df.columns = df.columns.str.strip()

# Map the DataFrame
df_final = pd.DataFrame()

df_final['app_id'] = df.iloc[:, 0]
df_final['title'] = df.iloc[:, 1]
df_final['price'] = pd.to_numeric(df.iloc[:, 6], errors='coerce').fillna(0.0)
df_final['description'] = df.iloc[:, 9]

# Updated indices for correct alignment
df_final['header_image'] = df.iloc[:, 13] 
df_final['developer'] = df.iloc[:, 33]
df_final['genres'] = df.iloc[:, 35]       
df_final['tags'] = df.iloc[:, 36]         
df_final['screenshot'] = df.iloc[:, 38]
df_final['metadata'] = df.iloc[:, 39]  

df_final['stock'] = 99
df_final['created_at'] = datetime.now()
df_final['created_by_id'] = None

# --- PRE-WRITE VERIFICATION ---
print("--- PRE-WRITE VERIFICATION ---")
print(f"Title:     {df_final['title'].iloc[0]}")
print(f"Price:     {df_final['price'].iloc[0]}")
print(f"Dev:       {df_final['developer'].iloc[0]}")
print(f"Image URL: {df_final['header_image'].iloc[0][:50]}...")
print(f"Screens:   {df_final['screenshot'].iloc[0][:50]}...")
print("------------------------------")

try:
    with engine.connect() as connection:
        # This is the MAGIC part to fix your error:
        print("Disabling foreign keys...")
        connection.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        
        print("Cleaning table and resetting IDs...")
        connection.execute(text("TRUNCATE TABLE game"))
        
        # Re-enable safety checks
        connection.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        connection.commit()

    print(f"Starting database dump of {len(df_final)} games...")
    # This will now execute because the truncate succeeded
    df_final.to_sql('game', con=engine, if_exists='append', index=False, chunksize=1000)
    print("Success: All data has been uploaded to the database.")
    
except Exception as e:
    print(f"SQL Error: {e}")