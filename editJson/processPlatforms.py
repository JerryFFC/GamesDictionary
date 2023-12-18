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
            new_row['concatenated_company_names'] = company
            new_row['concatenated_platform_names'] = platform
            # Add the new row to the list
            new_rows.append(new_row)

    # Create a new DataFrame from the list of new rows
    expanded_df = pd.DataFrame(new_rows)

    return expanded_df
