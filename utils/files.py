import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import os

def convert_to_pdf(input_file: str, output_file: str):
    file_extension = os.path.splitext(input_file)[1]
    
    if file_extension == '.csv':
        df = pd.read_csv(input_file)
    elif file_extension in ['.xls', '.xlsx']:
        df = pd.read_excel(input_file)
    else:
        raise ValueError("Unsupported file format")
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for i in range(len(df)):
        for j in range(len(df.columns)):
            pdf.cell(40, 10, txt=str(df.iat[i, j]), ln=0)
        pdf.ln(10)
    
    pdf.output(output_file)
    
def custom_analysis(input_file: str, columns: list):
    file_extension = os.path.splitext(input_file)[1]
    
    if file_extension == '.csv':
        df = pd.read_csv(input_file)
    elif file_extension in ['.xls', '.xlsx']:
        df = pd.read_excel(input_file)
    else:
        raise ValueError("Unsupported file format")
    
    if not set(columns).issubset(df.columns):
        raise ValueError("Selected columns not found in the file")

    analysis_result = {}
    
    for col in columns:
        analysis_result[col] = {
            "mean": df[col].mean(),
            "median": df[col].median(),
            "std": df[col].std(),
            "min": df[col].min(),
            "max": df[col].max(),
            "count": df[col].count()
        }
    
    return analysis_result

def clean_data(input_file: str, output_file: str):
    # to determine how to read the file
    file_extension = os.path.splitext(input_file)[1]
    
    if file_extension == '.csv':
        df = pd.read_csv(input_file)
    elif file_extension in ['.xls', '.xlsx']:
        df = pd.read_excel(input_file)
    else:
        raise ValueError("Unsupported file format")
    
    df_cleaned = df.drop_duplicates()
    
    # Drop rows with missing values
    df_cleaned = df_cleaned.dropna()
    
    # Save the cleaned data 
    if file_extension == '.csv':
        df_cleaned.to_csv(output_file, index=False)
    else:
        df_cleaned.to_excel(output_file, index=False)
