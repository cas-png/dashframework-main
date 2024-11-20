import plotly.express as px
import pandas as pd


def get_data():
    df= pd.read_excel('./jbi100_app/dataset/data.xlsx', index_col=0)
    # Any further data preprocessing can go her
    return df
