import pandas as pd
from fpdf import FPDF

def convert_to_pdf(input_file: str, output_file: str):
    df = pd.read_csv(input_file) if input_file.endswith('.csv') else pd.read_excel(input_file)
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for i, row in df.iterrows():
        line = ', '.join(str(value) for value in row)
        pdf.cell(200, 10, txt=line, ln=True, align='L')
    
    pdf.output(output_file)
    return output_file
