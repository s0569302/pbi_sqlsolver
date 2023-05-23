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
    with open("pbi_sqlsolver/files/converted_json.json", 'w') as file:
        json.dump(table_structure, file, indent=None, ensure_ascii=False)

    return table_structure


def generate_oracle_ddl(json_data):
    ddl_statements = []

    # Iterate over each table in the JSON data
    for table in json_data['tables']:
        table_name = table['name']
        columns = table['columns']

        # Generate the CREATE TABLE statement
        ddl = f"CREATE TABLE {table_name} (\n"

        # Generate the column definitions
        column_definitions = []
        for column in columns:
            column_name = column['name']
            data_type = column['type']
            primary_key = column['primary_key']
            foreign_key = column.get('foreign_key')

            # Generate the column definition
            column_def = f"  {column_name} {data_type}"

            # Add PRIMARY KEY constraint
            if primary_key:
                column_def += " PRIMARY KEY"

            # Add FOREIGN KEY constraint
            if foreign_key:
                foreign_table = foreign_key['table']
                foreign_column = foreign_key['column']
                column_def += f" REFERENCES {foreign_table}({foreign_column})"

            column_definitions.append(column_def)

        ddl += ",\n".join(column_definitions)
        ddl += "\n);"

        ddl_statements.append(ddl)

        with open("pbi_sqlsolver/files/oracle_ddl.sql", 'w') as file:
            file.write("\n\n".join(ddl_statements))

    return "\n\n".join(ddl_statements)
