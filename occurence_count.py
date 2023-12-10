import pandas as pd
import glob

# Chemin vers vos fichiers CSV
path = 'data/'  # Assurez-vous de remplacer par votre chemin de dossier
all_files = glob.glob(path + "/*.csv")

# Liste pour stocker les données de tous les fichiers
all_data = []

# Charger chaque fichier CSV
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    all_data.append(df)

# Fusionner toutes les données dans un seul DataFrame
combined_data = pd.concat(all_data, axis=0, ignore_index=True)

# Compter les occurrences de chaque pays
country_counts = combined_data['Country'].value_counts()

# Identifier les noms uniques de pays
unique_countries = combined_data['Country'].unique()

# Ouvrir un fichier texte pour l'écriture
# Ouvrir un fichier texte pour l'écriture avec l'encodage utf-8
with open('resultats_pays.txt', 'w', encoding='utf-8') as file:
    file.write("Occurrences de chaque pays:\n")
    file.write(country_counts.to_string())
    file.write("\n\nNoms uniques de pays:\n")
    # Convertir tous les éléments en chaînes de caractères avant de les joindre
    file.write('\n'.join(str(country) for country in unique_countries if pd.notna(country)))



print("Les résultats ont été enregistrés dans 'resultats_pays.csv'")
