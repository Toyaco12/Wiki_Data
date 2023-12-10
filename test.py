import pandas as pd
import os
import re

def normalize_country_name(name):
    # Vérifie si la valeur est NaN ou non-string
    if pd.isna(name) or not isinstance(name, str):
        return name
    # Normalisations et substitutions manuelles
    name = name.strip().upper()
    substitutions = {
        "USA": "UNITED STATES",
        "U.S.": "UNITED STATES",
        "UK": "UNITED KINGDOM",
        "U.K.": "UNITED KINGDOM",
        "SOUTH KOREA": "KOREA, SOUTH",
        "NORTH KOREA": "KOREA, NORTH",
        "RUSSIA": "RUSSIAN FEDERATION",
        # Ajoutez d'autres substitutions ici
    }
    for key, value in substitutions.items():
        name = name.replace(key, value)
    name = re.sub(r"\(.*\)|\*| |\[.*\]|\d", "", name).strip()
    return name

def merge_dataframes(data_folder):
    final_df = pd.DataFrame()
    for filename in os.listdir(data_folder):
        if filename.endswith('.csv'):
            df = pd.read_csv(os.path.join(data_folder, filename))
            df.iloc[:, 0] = df.iloc[:, 0].apply(normalize_country_name)
            df.rename(columns={df.columns[0]: 'Country'}, inplace=True)
            feature_name = filename.replace('.csv', '').replace('_', ' ').title()
            df.rename(columns={df.columns[1]: feature_name}, inplace=True)
            final_df = df if final_df.empty else pd.merge(final_df, df, on='Country', how='outer')
    return final_df

def clean_and_save_dataframe(final_df, output_path, missing_value_threshold=0.80):
    threshold = missing_value_threshold * len(final_df.columns)
    cleaned_df = final_df.dropna(thresh=threshold)
    cleaned_df.to_csv(output_path, index=False)
    print(f"Data cleaned and saved to {output_path}")

# Paramètres configurables
data_folder = "data/"
output_file = 'merged_data.csv'

# Fusion des données
merged_df = merge_dataframes(data_folder)

# Nettoyage et enregistrement des données
clean_and_save_dataframe(merged_df, output_file)

print("Script executed successfully.")
