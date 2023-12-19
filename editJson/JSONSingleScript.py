import json
from datetime import datetime

with open(r'C:\Users\jerry\OneDrive\Desktop\codeWork\GamesDictionary\2024GamesReleases.json', 'r', encoding='utf-8') as gamesJson:
    GamesDictionary = json.load(gamesJson)
unique_keys = set()

# Assuming GamesDictionary is a list of dictionaries
for game in GamesDictionary:
    for key in game.keys():
        unique_keys.add(key)

def get_all_keys(data):
    keys = set()
    if isinstance(data, dict):
        for key, value in data.items():
            keys.add(key)
            keys = keys.union(get_all_keys(value))
    elif isinstance(data, list):
        for item in data:
            keys = keys.union(get_all_keys(item))
    return keys

# Assuming GamesDictionary is your list of dictionaries
all_unique_keys = set()
for game in GamesDictionary:
    all_unique_keys = all_unique_keys.union(get_all_keys(game))

import pandas as pd
from pandas import json_normalize

# Flatten the nested structure
df = json_normalize(GamesDictionary)

def unixToDT(UnixStamp):
    UnixStamp = int(UnixStamp)
    UnixStamp = datetime.utcfromtimestamp(UnixStamp).strftime('%d-%m-%Y')
    return UnixStamp

df['first_release_date'] = df['first_release_date'].apply(unixToDT) 




import pandas as pd
from collections import Counter

def count_sorted_company_ids(df): #*****taken out of final script so far
    # Extract 'involved_companies' column to a list
    involved_companies_list = df['involved_companies'].to_list()

    # Initialize a list to store ids
    all_ids = []

    # Iterate over each sublist
    for sublist in involved_companies_list:
        # Check if the sublist is a list and not empty
        if isinstance(sublist, list) and sublist:
            first_dict = sublist[0]  # Get the first dictionary in the sublist
            all_ids.append(first_dict['id'])

    # Count occurrences and sort
    count = Counter(all_ids)
    sorted_count = count.most_common()

    return sorted_count

print(len(df))
print("Do with trial")


#df.to_excel(r'C:\Users\jerry\OneDrive\Desktop\codeWork\GamesDictionary\sampleoutput.xlsx', index=False)
import pandas as pd

def reshape_company_data(df, column_name):
    # Prepare lists for company IDs and names
    company_ids = []
    company_names = []

    # Determine the maximum number of companies in any row
    max_companies = max(len(row[column_name]) if isinstance(row[column_name], list) else 0 for _, row in df.iterrows())

    # Iterate through each row in the DataFrame
    for _, row in df.iterrows():
        if isinstance(row[column_name], list):
            ids = [item['company']['id'] for item in row[column_name] if 'company' in item and isinstance(item['company'], dict)]
            names = [item['company']['name'] for item in row[column_name] if 'company' in item and isinstance(item['company'], dict)]
        else:
            ids, names = [], []

        # Fill the remaining slots with None if less than max_companies
        ids.extend([None] * (max_companies - len(ids)))
        names.extend([None] * (max_companies - len(names)))

        company_ids.append(ids)
        company_names.append(names)

    # Add the new columns to the original DataFrame
    for i in range(max_companies):
        df[f'company_id_{i+1}'] = [ids[i] for ids in company_ids]
        df[f'company_name_{i+1}'] = [names[i] for names in company_names]

    return df

# Usage example:
# Assuming 'df' is your DataFrame and 'involved_companies' is the column of interest
df = reshape_company_data(df, 'involved_companies')
#print(df)
#df.to_excel(r'C:\Users\jerry\OneDrive\Desktop\codeWork\GamesDictionary\sampleOutputFlattened.xlsx', index=False)

import pandas as pd

def process_involved_companies(df, column_name):
    # Initialize lists for concatenated names and counts
    concatenated_names = []
    company_counts = []

    # Iterate through each row in the DataFrame
    for _, row in df.iterrows():
        if isinstance(row[column_name], list):
            # Extract company names, convert to lowercase, and concatenate
            names = [item['company']['name'].lower() for item in row[column_name] if 'company' in item and isinstance(item['company'], dict)]
            concatenated_names.append(", ".join(names))
            company_counts.append(len(names))
        else:
            concatenated_names.append("")
            company_counts.append(0)

    # Drop the original 'involved company ids' column
    df = df.drop(column_name, axis=1)

    # Add new columns to the DataFrame
    df['concatenated_company_names'] = concatenated_names
    df['company_count'] = company_counts

    return df

# Usage example:
# Assuming 'df' is your DataFrame and 'involved_companies' is the column of interest


def process_platforms(df, column_name):
    # Initialize lists for concatenated names and counts
    concatenated_names = []
    platform_counts = []

    # Iterate through each row in the DataFrame
    for _, row in df.iterrows():
        if isinstance(row[column_name], list):
            # Extract platform names and concatenate
            names = [item['name'] for item in row[column_name] if 'name' in item]
            concatenated_names.append(", ".join(names))
            platform_counts.append(len(names))
        else:
            concatenated_names.append("")
            platform_counts.append(0)

    # Add new columns for concatenated platform names and counts
    df['concatenated_platform_names'] = concatenated_names
    df['platform_count'] = platform_counts
    df.drop('platforms', axis=1, inplace=True)
    return df

def lowerList(GameNAme):
    GameNAme = GameNAme.lower()
    return GameNAme
lowerlist = df['name'].apply(lowerList).to_list()
print(lowerlist)
# Usage example:
# Assuming 'df' is your DataFrame and 'platforms' is the column of interest
# df = process_platforms(df, 'platforms')
# print(df)

df.insert(loc = 2,
          column = 'name lower',
          value = lowerlist)

df = process_involved_companies(df, 'involved_companies')
print(df.columns)
df = process_platforms(df, 'platforms')
print(df.head())

# import pandas as pd
# from itertools import product

# def expand_df(df):
#     # Create a list to collect new rows
#     new_rows = []

#     for _, row in df.iterrows():
#         # Split the concatenated company names and platform names
#         companies = row['concatenated_company_names'].split(", ") if row['concatenated_company_names'] else [""]
#         platforms = row['concatenated_platform_names'].split(", ") if row['concatenated_platform_names'] else [""]

#         # Create all combinations of companies and platforms
#         combinations = list(product(companies, platforms))

#         for company, platform in combinations:
#             # Create a new row for each combination
#             new_row = row.copy()
#             new_row['concatenated_company_names'] = company
#             new_row['concatenated_platform_names'] = platform
#             # Add the new row to the list
#             new_rows.append(new_row)

#     # Create a new DataFrame from the list of new rows
#     expanded_df = pd.DataFrame(new_rows)

#     return expanded_df


from itertools import product
import pandas as pd

def expand_df(df):
    # Create a list to collect new rows
    new_rows = []

    for _, row in df.iterrows():
        # Split the concatenated company names and platform names
        companies = row['concatenated_company_names'].split(", ") if row['concatenated_company_names'] else [""]
        platforms = row['concatenated_platform_names'].split(", ") if row['concatenated_platform_names'] else [""]

        # Create all combinations of companies and platforms
        combinations = list(product(companies, platforms))

        for company, platform in combinations:
            # Create a new row for each combination
            new_row = row.copy()
            new_row['company'] = company  # Individual company name
            new_row['platform'] = platform  # Individual platform name
            # Retain the original comma-separated lists
            new_row['original_concatenated_company_names'] = row['concatenated_company_names']
            new_row['original_concatenated_platform_names'] = row['concatenated_platform_names']
            # Add the new row to the list
            new_rows.append(new_row)

    # Create a new DataFrame from the list of new rows
    expanded_df = pd.DataFrame(new_rows)
    expanded_df=expanded_df.drop(['original_concatenated_company_names','original_concatenated_platform_names', 'company_id_1','company_name_1','company_id_2','company_name_2','company_id_3','company_name_3','company_id_4','company_name_4','company_id_5','company_name_5','company_id_6','company_name_6'], axis = 1)
    expanded_df=expanded_df.rename(columns={'first_release_date' : 'Release Date', 'name lower':'Game names (lower)', 'name':'Game name', 'concatenated_company_names':'Company conc.', 'company_count' : 'Company count', 'concatenated_platform_names': 'Platforms conc.', 'company':'Company ind.'
                                , 'platform':'Platform ind.', 'platform_count':'Platform count'})
    def renameCountWithString(currentText, text):
        newText = str(text) + ' ' + str(currentText)
        return newText
    
    expanded_df['Platform count'] = expanded_df['Platform count'].apply(lambda x: renameCountWithString(x, 'All Platforms.'))
    expanded_df['Company count'] = expanded_df['Company count'].apply(lambda x: renameCountWithString(x, 'Involved Companies.'))
    def replace_pc_text(column_name, df = expanded_df):
        # Replace 'PC (Microsoft Windows)' with 'PC' in the specified column
        df[column_name] = df[column_name].str.replace('PC \(Microsoft Windows\)', 'PC', regex=True)
        return df
    print(expanded_df.columns)
    expanded_df= replace_pc_text('Platforms conc.')
    expanded_df =replace_pc_text('Platform ind.')
    return expanded_df


df = expand_df(df)    
print(len(df))
# Usage example:
# Assuming 'df' is your DataFrame
# expanded_df = expand_df(df)
# print(expanded_df)



df.to_excel(r'C:\Users\jerry\OneDrive\Desktop\codeWork\GamesDictionary\sampleOutputFlattened2.xlsx', index=False)
