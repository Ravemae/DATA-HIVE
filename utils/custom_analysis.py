import pandas as pd

def custom_analysis(input_file: str, columns: list):
    df = pd.read_csv(input_file) if input_file.endswith('.csv') else pd.read_excel(input_file)
    analysis_result = df[columns].describe()
    return analysis_result.to_dict()
