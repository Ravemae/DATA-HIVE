import pandas as pd
from autoviz import AutoViz_Class
import os
import glob


# I want  it to save each 
def visualize_data(filepath, username):
    AV = AutoViz_Class()

    if not os.path.exists(filepath):
        return {'message': 'File does not exist'}
    try:
        data = pd.read_csv(filepath)
        csv_name = os.path.basename(filepath)
        save_dir = f"{username}_{csv_name.split('.')[0]}"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        dft = AV.AutoViz(
            "",
            sep=",",
            depVar="",
            dfte=data,
            header=0,
            verbose=2,
            lowess=False,
            chart_format="png",
            max_rows_analyzed=150000,
            max_cols_analyzed=30,
            save_plot_dir=save_dir
        )
        autoviz_dir = os.path.join(save_dir, "AutoViz")
        png_files = glob.glob(os.path.join(autoviz_dir, "*.png"))
        return {'visualized_files': png_files}


    except Exception as e:
        return {'message': str(e)}
    


print(  "##  Analysis of Sales Data: Unveiling Opportunities for Growth\n\nThis analysis dives into the sales data of a company selling various product lines like motorcycles, classic cars, planes, trains, and trucks. Let's break down the key findings and how they can help us make smarter business decisions.\n\n**1. Data Overview:**\n\nThe data includes information about individual orders placed by customers. Each row represents a single order. It details important information like the order number, quantity of items ordered, price per item, order line number, total sales, order date, status, quarter, month, and year of the order, the product line, MSRP, product code, customer name, customer phone, customer address, city, state, postal code, country, territory, contact person's last name and first name, and the size of the deal.\n\n**2. Key Trends:**\n\n* **Steady Growth:** The data shows a general upward trend in sales over time.  It's like watching a plant grow taller and stronger each month. \n* **Seasonal Fluctuations:** Sales peak during the last quarter of each year (Q4). This is like a surge in demand for holiday gifts during the festive season.\n* **Stronger Performance in US & Europe:**  The majority of sales come from the US and Europe, indicating these regions hold significant market potential. This is like having two strong branches of your business in different parts of the world.\n\n**3. Variable Relationships:**\n\n* **Quantity and Sales:**  Higher quantity ordered results in higher sales. This is like a simple equation – more products sold, more revenue generated.\n* **Deal Size and Product Line:** Some product lines, like Classic Cars and Motorcycles, tend to have larger deal sizes. This is like selling luxury items that attract customers willing to spend more.\n* **Status and Deal Size:** Cancelled orders often have smaller deal sizes compared to shipped orders. This is like losing out on potential profits when customers don't complete their purchases.\n\n**4. Standout Observations:**\n\n* **Highest Selling Product Line:**  Classic Cars contribute significantly to overall sales. It's like having a star product that's a real crowd-pleaser.\n* **Large Orders:**  A few orders have exceptionally high sales values, indicating potential for high-value customers. It's like having a few loyal customers who contribute significantly to your bottom line.\n* **Outliers:**  Some orders have unusually high quantities ordered, which might require further investigation. It's like finding an odd branch on your plant that needs extra attention.\n\n**5. Comparative Analysis:**\n\n* **Product Line Performance:** Classic Cars consistently outperform other product lines in terms of sales. It's like having a star athlete who consistently brings home medals.\n* **Regional Differences:**  Sales in the USA and Europe are significantly higher than in other regions. This is like having a city with a bustling market compared to a quieter town.\n* **Deal Size Distribution:**  Most deals are small, while a few large deals contribute significantly to the revenue. This is like having a busy farmer's market with lots of smaller purchases, but a few big orders from wholesale buyers.\n\n**6. Potential Impact Factors:**\n\n* **Product Line Popularity:**  Classic Cars might be more popular or in higher demand than other product lines.\n* **Marketing Efforts:**  Marketing strategies might be more effective in the USA and Europe, leading to higher sales.\n* **Seasonality:**  The holiday season could drive increased demand for certain product lines.\n\n**7. Actionable Insights:**\n\n* **Focus on High-Value Product Lines:**  Invest more in promoting and expanding the Classic Cars line, as it seems to be a strong revenue generator.\n* **Target High-Value Customers:**  Develop strategies to retain and attract high-value customers who place large orders, potentially through personalized marketing or loyalty programs.\n* **Increase Sales in Other Regions:**  Explore new marketing channels and strategies to tap into the potential of emerging markets outside the USA and Europe.\n* **Minimize Order Cancellations:** Analyze reasons for order cancellations and implement strategies to improve customer satisfaction and reduce lost sales.\n* **Optimize Inventory:**  Analyze product demand and sales patterns to optimize inventory levels and minimize overstocking or shortages.\n\n**8. Visual Representation Ideas:**\n\n* **Sales Trend Line Chart:**  A line chart showing sales growth over time would visually demonstrate the upward trend and seasonal fluctuations. \n* **Product Line Pie Chart:**  A pie chart showing the percentage of sales contributed by each product line would illustrate the dominance of Classic Cars.\n\n**9. Unexpected Findings:**\n\n* **High Sales Despite Cancellations:**  While cancellations exist, overall sales remain strong, suggesting a robust customer base and a good recovery rate from cancellations. This is like having a busy restaurant with some cancellations, but still enough guests to keep the business thriving.\n\n**10. Limitations and Further Investigation:**\n\n* **Limited Data:**  The analysis is based on order-level data and might not capture detailed customer behavior or market trends.\n* **Missing Information:**  Some address information is missing, hindering a thorough geographic analysis.\n* **Additional Data Points:**  Including customer demographics, marketing campaign data, and competitor information would provide a more comprehensive understanding of the market and customer behavior.\n\n**Conclusion:**\n\nThe sales data reveals promising opportunities for growth. By focusing on high-value product lines, targeting specific customer segments, and expanding into new markets, the company can optimize its performance and achieve its sales objectives. Further data collection and analysis can provide even more valuable insights for informed decision-making. \n")
    

