import plotly.express as px
import pandas as pd


def get_data():
    df= pd.read_excel('./jbi100_app/dataset/data.xlsx', index_col=0)
    df['Shark.common.name'] = df['Shark.common.name'].fillna("unknown")
    df['Victim.injury'] = df['Victim.injury'].replace(['injured', 'injury', 'Injured'], 'injury')
    df['Victim.activity'] = df['Victim.activity'].fillna("unknown")
    # Any further data preprocessing can go her
    return df
