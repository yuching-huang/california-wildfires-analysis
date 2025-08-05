"""
get_data.py
-----------
Module for fetching wildfire data from a given source and saving it locally.
"""

import logging
import os
import requests
import json

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

def fetch_ten_year_data(url: str, end_year: int = 2024):
    """
    Return 10-year fire incidents data in California, defaulting data from 2015 to 2024 and
    save the files (in json) each year to the folder: ../data/raw

    Args:
        url (string): the endpoint url of the API used for requesting the data
        end_year (int): the latest year of the data
    Return:
        None
    """
    logging.info(f"Fetching data from {url}")

    start_year = end_year - 9
    destination_folder = '../data/raw'
    os.makedirs(destination_folder, exist_ok=True)

    for year in range(start_year, end_year + 1):
        full_url = f'{url}{year}'

        try:
            response = requests.get(full_url)
            response.raise_for_status()
            file_path = os.path.join(destination_folder, f'fire_incidents_{year}.json')

            with open(file_path, 'w') as f:
                json.dump(response.json(), f, indent=4)
            logging.info(f"Saved data for {year} -> {file_path}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch data for year {year}: {e}")

if __name__ == '__main__':  # The url is no longer available
    url = 'https://incidents.fire.ca.gov/umbraco/api/IncidentApi/List?inactive=true&year='
    fetch_ten_year_data(url)
