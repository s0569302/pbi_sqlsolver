import openai
import pandas as pd
openai.api_key = "API-KEY"

def get_completion(prompt,model="gpt-3.5-turbo"):
    messages = [{"role":"user","content":prompt}]
    response = openai.ChatCompletion.create(
        model = model,
        messages = messages,
        temperature = 0
    )
    return response.choices[0].message["content"]

excel_file = pd.read_excel("pbi_sqlsolver/files/Table_Structure_Template.xlsx")
text = excel_file.to_string(index=False)
prompt = f"""
Your task is to provide me the SQL code, in text format, to create the tables based on the file {text}, without any introductory statements.
"""
response = get_completion(prompt)
print(response)