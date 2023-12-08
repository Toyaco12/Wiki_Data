import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO
import os

def find_country_column(columns):
    for col in columns:
        if 'country' in col.lower() or 'territory' in col.lower():
            return col
    return None

def extract_wikipedia_table_to_csv(url, output_file):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table in the HTML
    table = soup.find('table', {'class':'wikitable'})

    # Convert the HTML table to a string
    table_str = str(table)

    # Use StringIO to read the string as a file-like object
    df = pd.read_html(StringIO(table_str))[0]

    # Save the DataFrame to a CSV file
    df.to_csv(output_file, index=False)

def clean_date(input_file):
    # Charger le fichier CSV
    df = pd.read_csv(input_file)

    # Afficher les noms de colonnes avec un index
    print("Available columns:")
    for i, col in enumerate(df.columns, 1):
        print(f"{i}. {col}")

    # Identifier automatiquement la colonne du pays
    country_col = find_country_column(df.columns)
    if not country_col:
        country_col = input('Enter the country column name: ')

    # Afficher les 5 premières lignes
    print(df.head())

    # Demande à l'utilisateur de choisir le numéro d'une colonne
    column_index = int(input('Enter the number of the column you want to keep: ')) - 1

    # Vérifier si le numéro de colonne est valide
    if column_index < 0 or column_index >= len(df.columns):
        print("Invalid column number. Please try again.")
        os.remove('tmp.csv')
        exit(1)

    column_to_keep = df.columns[column_index]

    result_df = df[[country_col, column_to_keep]]

    # Enregistrer le DataFrame dans un fichier CSV et demander à l'utilisateur de choisir un nom de fichier
    output_file = input('Enter a file name: ')

    #Ajouter .csv à la fin du nom de fichier
    output_file += '.csv'

    result_df.to_csv(output_file, index=False)

    #supprimer le fichier tmp.csv
    os.remove('tmp.csv')

# Demande à l'utilisateur de saisir une URL
url = input('Enter a URL: ')

# Name of the output CSV file
output_file = 'tmp.csv'

extract_wikipedia_table_to_csv(url, output_file)
clean_date(output_file)


