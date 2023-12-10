import pandas as pd
import os
import re

# Fonction pour normaliser les noms des pays
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

# Chemin vers le dossier contenant les fichiers CSV
data_folder = "data/"

final_df = pd.DataFrame()

# Lire chaque fichier CSV, le normaliser et le fusionner
for filename in os.listdir(data_folder):
    if filename.endswith('.csv'):
        df = pd.read_csv(os.path.join(data_folder, filename))
        df.iloc[:, 0] = df.iloc[:, 0].apply(normalize_country_name)
        df.rename(columns={df.columns[0]: 'Country'}, inplace=True)
        feature_name = filename.replace('.csv', '')
        df.rename(columns={df.columns[1]: feature_name}, inplace=True)

        if final_df.empty:
            final_df = df
        else:
            final_df = pd.merge(final_df, df, on='Country', how='outer')

# Supprimer les lignes avec plus de 20% de valeurs manquantes
threshold = 0.80 * len(final_df.columns)
final_df = final_df.dropna(thresh=threshold)

# Supprime ce qu'il y'a entre () et [] de chaque case
final_df = final_df.replace(to_replace='\(.*\)|\[.*\]', value='', regex=True)
# Supprime les espaces a la fin de chaque case
final_df = final_df.replace(to_replace='\s$', value='', regex=True)

final_df.to_csv('merged_data.csv', index=False)

print("Fusion terminée avec suppression des lignes ayant plus de 20% de valeurs manquantes. Les données sont enregistrées dans 'merged_data.csv'.")
