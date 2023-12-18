import json
from datetime import datetime
from .getUniqueDictKeys import uniqueKey
from .getAllKeys import get_all_keys
import pandas as pd
from pandas import json_normalize
from .companyProcessing import process_involved_companies, reshape_company_data
from .processPlatforms import process_platforms,flattenCompaniesAndPlatforms

def transformJson(GamesDictionaryJSON):
    unique_keys = set()
    # Assuming GamesDictionary is a list of dictionaries
    print(unique_keys)
    print(GamesDictionaryJSON)
    uniqueKey(GamesDictionaryJSON, unique_keys)
    print(unique_keys)

    # Assuming GamesDictionary is your list of dictionaries
    all_unique_keys = set()

    for game in GamesDictionaryJSON:
        all_unique_keys = all_unique_keys.union(get_all_keys(game))

    def unixToDT(UnixStamp):
        UnixStamp = int(UnixStamp)
        UnixStamp = datetime.utcfromtimestamp(UnixStamp).strftime('%d-%m-%Y')
        return UnixStamp

    # Flatten the nested structure
    df = json_normalize(GamesDictionaryJSON)

    df['first_release_date'] = df['first_release_date'].apply(unixToDT) 

    def lowerList(column):
        column = column.lower()
        return column
    lowerlist = df['name'].apply(lowerList).to_list()


    df.insert(loc = 2, column = 'name lower', value = lowerlist)

    df = process_involved_companies(df, 'involved_companies')
    df = process_platforms(df, 'platforms')
    df = flattenCompaniesAndPlatforms(df) 
    return df   

# with open(r'C:\Users\jerry\OneDrive\Desktop\codeWork\GamesDictionary\2024GamesReleases.json', 'r', encoding='utf-8') as gamesJson:
#     GamesDictionary = json.load(gamesJson)

#df = transformJson(GamesDictionary)
##df.to_excel(r'C:\Users\jerry\OneDrive\Desktop\codeWork\GamesDictionary\currentSample.xlsx', index=False)
