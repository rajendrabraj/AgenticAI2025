
## This program reads the JSON file and converts it to HTML file format.
## Works on Python version 3.13 

import pandas as pd
import json
from itertools import zip_longest


def json_to_html_table(json_file_path, html_file_path):
    """
    Reads a JSON file, converts it to a pandas DataFrame, 
    and saves it as an HTML file with all columns.
    
    Args:
        json_file_path (str): Path to the input JSON file.
        html_file_path (str): Path for the output HTML file.
    """
    try:
        # Read the JSON file into a pandas DataFrame
        # The 'orient="records"' is often necessary if the JSON file 
        # is a list of objects, which is common for tabular data
        print(html_file_path)
        print(f"JSON File Input : {json_file_path}")

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

        print(f"Successfully read JSON file: {json_file_path}")
        # print(df)
        
        # Convert the DataFrame to an HTML string
        # header=True ensures column names are included
        # index=False prevents pandas from adding an extra index column
        print(f"Initiating conversion  to HTML")

        html_table = df.to_html(header=True, index=False)
        # print(html_table)  # Print the HTML table string to the console for verification
        ## Extract columns and records for custom HTML generation

        columns = df.columns.tolist()
        records = df.to_dict('records')
        
        # print(f"Columns: {columns}")
        # print(f"Records: {records}")


        html = """
            <html>
            <head>
                <title>JSON to HTML Table</title>
                <style>
                    table { border-collapse: collapse; width: 100%; }
                    th, td { border: 1px solid #999; padding: 8px; text-align: left; }
                    th { background-color: #f2f2f2; }
                </style>
            </head>
            <body>
                <h2>Transaction Data</h2>
                <table>
                    <tr>
            """

        # Table headers
        for col in columns:
            html += f"<th>{col}</th>"

        html += "</tr>"

        # Table rows
        for record in records:
            html += "<tr>"
            for col in columns:
                html += f"<td>{record.get(col, '')}</td>"
            html += "</tr>"

        html += """
            </table>
        </body>
        </html>
        """

    
        full_html_content = html  # Use the custom HTML generated above

        
        # Write the HTML string to a file
        with open(html_file_path, 'w') as f:
            f.write(full_html_content)

        print("====" * 20)            
        print(f"Successfully converted '{json_file_path}' to '{html_file_path}'")
        print("====" * 20)


    except ValueError as e:
        print(f"Error reading JSON file. Details: {e}")
    except FileNotFoundError:
        print(f"Error: The file '{json_file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")





# with open('data.json', 'w') as f:
#     json.dump(dummy_json_data, f)

# # 2. Run the conversion
# json_file = 'data.json'
# html_file = 'output.html'
# json_to_html_table(json_file, html_file)
