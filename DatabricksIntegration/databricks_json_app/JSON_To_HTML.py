import pandas as pd
import json

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
        df = pd.read_json(json_file_path, orient='records')
        print(f"Successfully read JSON file: {json_file_path}")


        # Convert the DataFrame to an HTML string
        # header=True ensures column names are included
        # index=False prevents pandas from adding an extra index column
        print(f"Converted to HTML")
        html_table = df.to_html(header=True, index=False)
        print(html_table)  # Print the HTML table string to the console for verification

        

        # Add basic HTML structure for better viewing
        full_html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>JSON to HTML Table</title>
            <style>
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h2>Data from JSON file</h2>
            {html_table}
        </body>
        </html>
        """
        
        # Write the HTML string to a file
        with open(html_file_path, 'w') as f:
            f.write(full_html_content)
            
        print(f"Successfully converted '{json_file_path}' to '{html_file_path}'")
        print("====" * 20)


    except ValueError as e:
        print(f"Error reading JSON file. Ensure it is a valid JSON list of objects. Details: {e}")
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
