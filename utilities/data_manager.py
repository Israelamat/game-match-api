import os 
import requests

def ensure_dataset_exists(local_path: str, url:str):
    os.makedirs("data", exist_ok=True)

    if os.path.exists(local_path):
        print(f"CSV found in {local_path}, using it...")
        return True
    print(f"CSV not found in {local_path}, downloading it from github...")
    
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        with open(local_path, "wb") as f:
            f.write(r.content)
        print(f"CSV downloaded and saved in {local_path}")
        return True
    
    except Exception as e:
        print(f"Error downloading CSV: {e}")
    return False
    