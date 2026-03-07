from sqlalchemy import create_engine
from dotenv import load_dotenv;
import os 
from pathlib import Path

load_dotenv();
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
DATABASE_URL = os.getenv("DATABASE_URL")

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("Succesful Connection! Pyhton can write at the symfony Database")
    connection.close()
except Exception as e:
    print(f"Error To connect: {e}")