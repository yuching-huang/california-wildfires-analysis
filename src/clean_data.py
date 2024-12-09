from typing import List
import os
import pandas as pd
from pandas import DataFrame


def get_years() -> List[int]:
    """
    Obtain the years of the data fetched in the raw data folder in ascending order

    Returns:
        years_obtained (List of int): Sorted list of years
    """
    folder_path = '../data/raw'
    file_names = os.listdir(folder_path)

    years_obtained = []
    for name in file_names:
        # excluding other files if necessary
        if name.startswith('fire_incidents_') and name.endswith(".json"):
            year = name.split('_')[2].split('.')[0]
            years_obtained.append(year)

    return sorted(list(map(int, years_obtained)))

def combine_data(years_obtained: list[int]) -> DataFrame:
    """
    Combine the raw data obtained in the raw folder

    Args:
        years_obtained (List[int]): List of the years of data obtained in the raw folder
    Returns:
        combined_df (DataFrame): Combined DataFrame
    """
    irrelevant_cols = ['Final', 'Updated', 'AdminUnit','AdminUnitUrl', 'ControlStatement', 'ControlStatement',
                       'AgencyNames', 'Type', 'UniqueId', 'StartedDateOnly', 'ExtinguishedDateOnly',
                       'Url', 'IsActive', 'CalFireIncident', 'NotificationDesired']

    combined_df = pd.DataFrame()

    for year in years_obtained:
        file_path = f'../data/raw/fire_incidents_{year}.json'

        with open(file_path, 'r') as file:
            df_single_year = pd.read_json(file)
            # Drop columns that are not relevant to the analysis I'm focusing on for this project
            df_single_year.drop(columns=irrelevant_cols, errors='ignore', inplace=True)

        combined_df = pd.concat([combined_df, df_single_year], ignore_index=True)

    return combined_df

def clean_and_save_data(df):
    """
    Clean and save dataset to the data/processed folder

    :param df (Pandas DataFrame): Input Dataframe
    """
    # Add Year Column to the Dataset by extracting the year from 'Started'
    df['Year'] = pd.to_datetime(df['Started'], errors='coerce').dt.year.astype(int)

    # Drop data if the year is not in the range of 2015-2024
    df = df[(df['Year'] >= 2015) & (df['Year'] <= 2024)]

    # Add Extinguished Time to the Dataset
    df['Started'] = pd.to_datetime(df['Started'], errors='coerce')
    df['ExtinguishedDate'] = pd.to_datetime(df['ExtinguishedDate'], errors='coerce')
    df['ExtinguishedTime'] = df['ExtinguishedDate'] - df['Started']
    df['ExtinguishedTime'] = df['ExtinguishedTime'].dt.total_seconds() / 3600

    # Drop ExtinguishedDate after calculating duration
    df = df.drop('ExtinguishedDate', axis=1)

    # Fill missing ExtinguishedTime with mean Extinguished Time
    extinguished_mean = df['ExtinguishedTime'].mean()
    df['ExtinguishedTime'] = df['ExtinguishedTime'].fillna(extinguished_mean)

    # County: include only the County name (without city name) and drop the rows with missing County Name
    df['County'] = df['County'].fillna('').astype(str)
    df['County'] = df['County'].apply(lambda x: x.split(',')[-1].strip() if x else '')
    df = df[df['County'] != '']

    # AcresBurned: Fill missing values with overall average value
    acre_mean = df['AcresBurned'].mean()
    df['AcresBurned'] = df['AcresBurned'].fillna(acre_mean)

    # PercentContained: Fill missing values with overall average
    pc_mean = df['PercentContained'].mean()
    df['PercentContained'] = df['PercentContained'].fillna(pc_mean)

    folder_path = '../data/processed/'
    file_name = 'fire_incidents_data.csv'
    df.to_csv(folder_path + file_name, index=False)

if __name__ == '__main__':
    years_obtained = get_years()
    combined_df = combine_data(years_obtained)
    clean_and_save_data(combined_df)
