import pandas as pd

def clean_data(input_file: str, output_file: str):
    df = pd.read_csv(input_file) if input_file.endswith('.csv') else pd.read_excel(input_file)
    df = df.dropna()  
    df.to_csv(output_file, index=False) if input_file.endswith('.csv') else df.to_excel(output_file, index=False)
    return output_file
