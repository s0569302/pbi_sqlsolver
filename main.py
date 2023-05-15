import helpers

excel_file = "files\Table_Structure_Template.xlsx"
json_data = helpers.excel_to_json(excel_file)
ddl_code = helpers.generate_oracle_ddl(json_data)