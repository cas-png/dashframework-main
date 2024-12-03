import plotly.express as px
import pandas as pd


def get_data():
    df= pd.read_excel('./jbi100_app/dataset/data.xlsx', index_col=0)
    df['Shark.common.name'] = df['Shark.common.name'].fillna("unknown")
    df['Victim.injury'] = df['Victim.injury'].replace(['injured', 'injury', 'Injured'], 'injury')
    df['Victim.activity'] = df['Victim.activity'].fillna("unknown")
    df2=pd.DataFrame({'month':df['Incident.month'], 'year':df['Incident.year']})
    df['Incident.date']=pd.to_datetime(df2[['year','month']].assign(day=1))
    # Any further data preprocessing can go here
    return df
