import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO
import os
import re

def find_country_column(columns):
    pattern = re.compile(r'\bcountry\b|\bterritory\b|\bcountries\b|\blocation\b', re.IGNORECASE)
    for col in columns:
        if pattern.search(col):
            return col
    return None

def extract_wikipedia_table_to_csv(url, output_file):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all tables in the HTML
    tables = soup.find_all('table', {'class':'wikitable'})

    # Check if there are multiple tables
    if len(tables) > 1:
        print(f"{len(tables)} tables found. Please choose which table to extract:")

        # Show a preview of each table
        for i, table in enumerate(tables, 1):
            table_str = str(table)
            df_preview = pd.read_html(StringIO(table_str))[0]
            print(f"\nTable {i} Preview:")
            print(df_preview.head())

        # Ask the user to choose a table
        table_choice = int(input("\nEnter the number of the table you want to extract: ")) - 1

        # Validate the choice
        if table_choice < 0 or table_choice >= len(tables):
            print("Invalid table number. Exiting.")
            exit(1)
    else:
        table_choice = 0

    # Convert the chosen HTML table to a string
    table_str = str(tables[table_choice])

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


