"""
This module contains a function to read and process the shark attack data from an Excel file.
"""
import pandas as pd


def get_data():
    """
    Reads and processes shark attack data from an Excel file.
    
    The function performs the following operations:
    - Reads data from an Excel file located at './jbi100_app/dataset/data_modified_new.xlsx'.
    - Creates a new column 'index1' with the index values for selection highlights in the app.
    - Fills missing values in 'Shark.common.name', 'Victim.activity', 'Injury.severity', 'Victim.gender', 
      'Data.source', 'Provoked/unprovoked', and 'Shark.full.name' columns with "unknown".
    - Standardizes values in 'Victim.injury' and 'Injury.severity' columns.
    - Removes commas from 'Incident.year' column and converts it to integer type.
    - Creates a new column 'Incident.date' with the date of the incident, set to the first day of the month.
    
    Additionally, the excel file was manually modified to include the 'Shark.full.name' column as "Shark.common.name (Shark.scientific.name)", and modified:
    The Shark.full.name column was MANUALLY added and modified in the following ways:
    - row 439 was "unknown (Orectolobidae)", replaced by "wobbegong (Orectolobidae)"
    - all variations of "[broadnose ]seven[ ]gill shark (Notorynchus cepedianus)" were replaced by "broadnose sevengill shark (Notorynchus cepedianus)"
    - all variations of "whaler shark ([])" were replaced by "whaler shark (Carcharhinidae)"
    - row 1223 was "lemon shark", replaced by "lemon shark (Negaprion brevirostris)"
    
    Returns:
    - pd.DataFrame: A pandas DataFrame containing the processed shark attack data.
    """
    df= pd.read_excel('./jbi100_app/dataset/data_modified_new.xlsx', index_col=0) # read data from excel file
    df['index1'] = df.index # create a new column with the index values, used for selection highlights in the app
    df['Shark.common.name'] = df['Shark.common.name'].fillna('unknown') # fill missing values with 'unknown'
    df['Victim.injury'] = df['Victim.injury'].replace(['injured', 'injury', 'Injured'], 'injured') # standardize injury result names
    df['Victim.activity'] = df['Victim.activity'].fillna('unknown') # fill missing values with 'unknown'
    df['Injury.severity'] = df['Injury.severity'].replace(['fatal', 'fatality'], 'fatal') # standardize injury severity names
    df['Injury.severity'] = df['Injury.severity'].fillna('unknown') # fill missing values with 'unknown'
    df['Victim.gender'] = df['Victim.gender'].fillna('unknown') # fill missing values with 'unknown'
    df['Data.source'] = df['Data.source'].fillna('unknown') # fill missing values with 'unknown'
    df['Provoked/unprovoked'] = df['Provoked/unprovoked'].fillna('unknown') # fill missing values with 'unknown'
    df['Incident.year'] = df['Incident.year'].astype(str).str.replace(',', '').astype(int) # remove commas and convert to int
    df['Shark.full.name'] = df['Shark.full.name'].fillna('unknown') # fill missing values with 'unknown'
    df2=pd.DataFrame({'month':df['Incident.month'], 'year':df['Incident.year']}) # create an auxiliary dataframe with the month and year columns
    df['Incident.date']=pd.to_datetime(df2[['year','month']].assign(day=1)) # create a new column with the date of the incident, set to first day of the month
    return df
