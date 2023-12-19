import pandas as pd
from itertools import product


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

# def flattenCompaniesAndPlatforms(df):
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
def flattenCompaniesAndPlatforms(df):
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
    expanded_df=expanded_df.drop(['original_concatenated_company_names','original_concatenated_platform_names'], axis = 1)
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