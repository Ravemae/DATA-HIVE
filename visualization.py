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
    


  

