import pandas as pd
import json
from itertools import zip_longest

import pandas as pd


## This program reads the JSON file and converts it to CSV file format.
## Works on Python version 3.13 


def json_to_csv(json_file_path, csv_file_path):
    
    
    try:
        # Read the JSON file into a pandas DataFrame
        # The 'orient="records"' is often necessary if the JSON file 
        # is a list of objects, which is common for tabular data
        print(csv_file_path)
        print(f"JSON File Input : {json_file_path}")

        # Load JSON safely using the json module so we can handle varied structures
        # with open(json_file_path, 'r', encoding='utf-8') as jf:
          
           # Load JSON safely using the json module so we can handle varied structures
        with open(json_file_path, 'r', encoding='utf-8') as jf:
            data = json.load(jf)


        # Normalize different possible JSON shapes into a list of records
        if isinstance(data, dict):
            # Common case: { "records": [ ... ] }
            if 'records' in data and isinstance(data['records'], list):
                records = data['records']
            else:
                # If it's a dict of lists with potentially different lengths,
                # convert to list-of-dicts by zipping with fillvalue=None
                if all(isinstance(v, list) for v in data.values()):
                    keys = list(data.keys())
                    rows = []
                    for vals in zip_longest(*data.values(), fillvalue=None):
                        rows.append(dict(zip(keys, vals)))
                    records = rows
                else:
                    # Fallback: wrap single dict as one record
                    records = [data]
        elif isinstance(data, list):
            records = data
        else:
            records = [data]

        # Use json_normalize to flatten nested objects where possible
        df = pd.json_normalize(records)

        # Convert any list/dict cells to JSON strings to avoid DataFrame construction errors
        def _stringify_complex(v):
            if isinstance(v, (list, dict)):
                try:
                    return json.dumps(v, ensure_ascii=False)
                except Exception:
                    return str(v)
            return v

        df = df.applymap(_stringify_complex)        
        df.to_csv(csv_file_path, index=False)

        print(f"Successfully read CSV file: {json_file_path}")
        
        print("====" * 20)            
        print(f"Successfully converted '{json_file_path}' to '{csv_file_path}'")
        print("====" * 20)


    except ValueError as e:
        print(f"Error reading JSON file. Details: {e}")
    except FileNotFoundError:
        print(f"Error: The file '{json_file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


