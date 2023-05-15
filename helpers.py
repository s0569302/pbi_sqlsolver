import pandas as pd
import json

def excel_to_json(excel_file):
    # Read the Excel file into a Pandas DataFrame
    df = pd.read_excel(excel_file)

    # Create a dictionary to store the table structure
    table_structure = {"tables": []}

    # Iterate over each table worksheet in the Excel file
    for table_name in df['Table Name'].unique():
        table_data = {"name": table_name, "columns": []}

        # Filter the DataFrame for the current table
        table_df = df[df['Table Name'] == table_name]

        # Iterate over each row in the filtered DataFrame
        for _, row in table_df.iterrows():
            column = {
                "name": row['Column Name'],
                "type": row['Data Type'],
                "primary_key": True if row['Primary Key'] == 'Yes' else False
            }

            if pd.notnull(row['Foreign Key']):
                column["foreign_key"] = {
                    "table": row['Foreign Key'].split('.')[0],
                    "column": row['Foreign Key'].split('.')[1]
                }

            table_data["columns"].append(column)

        table_structure["tables"].append(table_data)

    # Write the table structure JSON directly to the file
    with open("files/converted_json.json", 'w') as file:
        json.dump(table_structure, file, indent=None, ensure_ascii=False)

    return table_structure