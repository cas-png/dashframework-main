import plotly.express as px
import pandas as pd


def get_data():
    df= pd.read_excel('./jbi100_app/dataset/data_modified_new.xlsx', index_col=0)
    df['Shark.common.name'] = df['Shark.common.name'].fillna("unknown") # fill missing values with "unknown"
    df['Victim.injury'] = df['Victim.injury'].replace(['injured', 'injury', 'Injured'], 'injured') # standardize injury names
    df['Victim.activity'] = df['Victim.activity'].fillna("unknown") # fill missing values with "unknown"
    df['Incident.year'] = df['Incident.year'].astype(str).str.replace(',', '').astype(int) # remove commas and convert to int
    df['Shark.full.name'] = df['Shark.full.name'].fillna("unknown")
    #df['Shark.full.name'] is generated in the excel file as Shark.common.name + " (" + Shark.scientific.name + ")"
    # additionally: - row 439 was "unknown (Orectolobidae)", replaced by "wobbegong (Orectolobidae)"
    #               - all variations of "[broadnose ]seven[ ]gill shark (Notorynchus cepedianus)" were replaced by "broadnose sevengill shark (Notorynchus cepedianus)"
    #               - all variations of "whaler shark ([])" were replaced by "whaler shark (Carcharhinidae)"
    #               - row 1223 was "lemon shark", replaced by "lemon shark (Negaprion brevirostris)"
    # Any further data preprocessing can go here
    df2=pd.DataFrame({'month':df['Incident.month'], 'year':df['Incident.year']})
    df['Incident.date']=pd.to_datetime(df2[['year','month']].assign(day=1))
    return df
