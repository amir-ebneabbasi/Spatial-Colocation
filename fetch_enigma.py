import io
from pathlib import Path
import pandas as pd
import requests

RAW_BASE_URL = "https://raw.githubusercontent.com/MICA-MNI/ENIGMA/master/enigmatoolbox/datasets/summary_statistics"
API_URL = "https://api.github.com/repos/MICA-MNI/ENIGMA/contents/enigmatoolbox/datasets/summary_statistics"

def fetch_summary_stats(save_local=False, save_dir="./summary_statistics"):

    data = {}
    
    if save_local:
        Path(save_dir).mkdir(parents=True, exist_ok=True)

    try:
        resp = requests.get(API_URL)
        resp.raise_for_status()
        tree = resp.json()
    except Exception as e:
        print(f"Failed to fetch repository file tree: {e}")
        return data

    csv_files = [item['name'] for item in tree if item['type'] == 'file' and item['name'].endswith('.csv')]

    _FILES = {}
    for filename in csv_files:
        prefix = filename.split('_')[0].lower()
        if prefix not in _FILES:
            _FILES[prefix] = {}
        
        key = filename.replace('.csv', '')
        _FILES[prefix][key] = filename

    for disorder, files in _FILES.items():
        data[disorder] = {}
        for key, filename in files.items():
            raw_url = f"{RAW_BASE_URL}/{filename}"
            try:
                response = requests.get(raw_url)
                response.raise_for_status()
                
                df = pd.read_csv(io.StringIO(response.text), on_bad_lines="skip")
                data[disorder][key] = df
                
                if save_local:
                    out_path = Path(save_dir) / filename
                    out_path.write_text(response.text, encoding='utf-8')
                    
                print(f"Successfully loaded: [{disorder}] {key}")
            except Exception as e:
                print(f"Failed to download [{disorder}] {key} ({filename}): {e}")
                
    return data

# Usage Example:
# if __name__ == "__main__":
#     summary_data = fetch_summary_stats(save_local=True)
