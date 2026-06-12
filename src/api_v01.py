#  get 50k rows of data and create 'cats_data_filtered.csv'
#  Claude helped implement safeguards against being disconnected

import os
import requests
import pandas as pd
from dotenv import load_dotenv
import time

load_dotenv()

API_KEY = os.getenv("API_KEY")

def get_data():
    
    viewName = 'cats'
    limit = 250
    page = 1
    all_cats = []

    headers = {
        "Content-Type": "application/vnd.api+json",
        "Authorization": API_KEY
    }

    while True:
        print(f"Pulling page {page}...")

        url = (
            f"https://api.rescuegroups.org/v5/"
            f"public/animals/"
            f"search/{viewName}/"
            f"?limit={limit}"
            f"&page={page}"
        )

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            

        except Exception as e:
            print(f"Error on page {page}: {e} — retrying in 5s...")
            time.sleep(5)
            continue  # retry the same page

        for item in data['data']:
            row = {'id': item['id']}
            row.update(item['attributes'])
            all_cats.append(row)

        print(f"  Got {len(data['data'])} records. Total so far: {len(all_cats)}")

        if len(all_cats) >= 50_000:                                         
            print("Reached 50k rows, stopping.")
            break

        if len(data['data']) < data['meta']['limit']:
            break

        page += 1
        time.sleep(1)

    df_cats = pd.DataFrame(all_cats)

    #  Change data type and create dependent variable
    df_cats['adoptedDate'] = pd.to_datetime(df_cats['adoptedDate'], errors='coerce')
    df_cats['availableDate'] = pd.to_datetime(df_cats['availableDate'], errors='coerce')
    df_cats['length_of_stay'] = (df_cats['adoptedDate'] - df_cats['availableDate']).dt.days
    print('Initial Data Retrieved:')
    df_cats.info()
    print('-------------------------------------------')

    df_filtered = df_cats[['id','sex','sizeCurrent','sizeGroup', 'sizeUOM', 'ageGroup', 'ageString','breedString','colorDetails', 'vocalLevel', 'sheddingLevel', 'energyLevel', 'exerciseNeeds', 'isSpecialNeeds', 'isCurrentVaccinations', 'isDeclawed', 'isHousetrained', 'isKidsOk', 'adultSexesOk','obedienceTraining', 'ownerExperience', 'newPeopleReaction', 'pictureCount', 'videoCount', 'adoptedDate', 'availableDate', 'length_of_stay']]
    df_filtered.to_csv('data/raw/anna_data_filtered.csv', index=False)
    print('Filtered Data:')
    df_filtered.info()