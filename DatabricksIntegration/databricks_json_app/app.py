## Rajendra Bichu
## Date :  Feb 2026 , this program connects to Databricks, executes a query, saves the results in JSON format, and converts it to an HTML table.


import json
from databricks_client import execute_query
from JSON_To_HTML import json_to_html_table


def main():
    query = """
        SELECT *
        FROM workspace.default.retail_data
        LIMIT 100
    """

    result = execute_query(query)
    print("Executing the query and fetching results...")
    print("--" * 50)

    #JSON File Path

    json_file_path= "C:\\Rajendra_2015\\AgenticAI_Programs\\Agentic_Batch2\\2-Langchain Basics\\11_IIT_Madras\\1_0_My_DataBricks_Assignment\\output.json"

    
    # Save JSON output to file
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, default=str)

    print(json.dumps(result, indent=4, default=str))
    f.close()

    print("Main JSON File is Closed.")

    print("Query Execution Complete.")

    print("--" * 50)


    ## Export JSON to HTML Table

    # print("Converting JSON to HTML Table.")
    # print("--" * 50)
    # json_file_path= "C:\\Rajendra_2015\\AgenticAI_Programs\\Agentic_Batch2\\2-Langchain Basics\\11_IIT_Madras\\1_0_My_DataBricks_Assignment\\output.json"
    # html_file_path= "C:\\Rajendra_2015\\AgenticAI_Programs\\Agentic_Batch2\\2-Langchain Basics\\11_IIT_Madras\\1_0_My_DataBricks_Assignment\\Records.html"

    # json_to_html_table(json_file_path, html_file_path)

    # print("Created HTML file.")


if __name__ == "__main__":
    main()

