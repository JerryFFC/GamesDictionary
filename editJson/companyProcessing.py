
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