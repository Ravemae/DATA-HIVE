import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

def insights(file):
    data = pd.read_csv(file).to_string()

    genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
# Choose a model that's appropriate for your use case.
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""{data}
    Given the provided CSV data, please analyze it as a data analyst would when presenting insights to a non-technical manager. Your analysis should include:

1. Data Overview: Briefly describe the type of data and its key components.

2. Key Trends: Identify and explain the most significant patterns or changes observed in the data.

3. Variable Relationships: Highlight any important connections between different data points.

4. Standout Observations: Point out any notably high or low values, outliers, or unusual patterns.

5. Comparative Analysis: If applicable, compare different categories, time periods, or segments within the data.

6. Potential Impact Factors: Suggest possible reasons for the observed trends or patterns.

7. Actionable Insights: Provide at least 3-5 practical, data-driven recommendations based on your analysis.

8. Visual Representation Ideas: Describe how you would visualize 1-2 key insights to make them more understandable.

9. Unexpected Findings: Mention any surprising or counterintuitive insights from the data.

10. Limitations and Further Investigation: Note any areas where the data might be insufficient and suggest additional data points that could enhance the analysis.

Please explain all concepts in plain language, avoiding technical jargon. Use analogies or real-world examples where appropriate to make the insights more relatable.

Your analysis should be thorough yet accessible, providing valuable insights that could directly impact decision-making. Aim for a balance between high-level overview and specific, actionable details.

If you need any clarification about specific columns or data points, please ask."""
    prompt2 = f"""{data}
Imagine you're the data analyst for our company. You've just analyzed our latest data and need to present your findings to the CEO in a brief, clear meeting. Your goal is to provide practical insights and actionable recommendations. Please structure your response as follows:

1. Brief Data Summary: In one sentence, what kind of data did you look at?

2. Three Key Findings: What are the most important things you discovered? Explain each in 1-2 simple sentences.

3. What This Means for Us: How do these findings impact our business? Use plain language and real-world examples.

4. Recommendations: Give 3 specific, practical actions we should take based on this data. Be clear about what to do and why.

5. One Surprise: What's one unexpected thing you found? Why is it interesting?

6. Next Steps: What's one area we should investigate further, and why?

Remember, you're talking directly to the CEO. Use simple language, avoid jargon, and focus on what matters for the business. Be confident in your analysis and recommendations."""
    response = model.generate_content(prompt)
    if response.text:
        analysis_text = response.text
    return {"analysis": analysis_text}
    

# print(insights('sales_data_sample.csv'))
