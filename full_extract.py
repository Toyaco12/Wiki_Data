import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO
import os
import re


# To find the right country column
def find_country_column(columns):
    pattern = re.compile(r'\bcountry\b|\bterritory\b|\bcountries\b|\blocation\b', re.IGNORECASE)
    for col in columns:
        if pattern.search(col):
            return col
    return None

# First extract from wikipedia
def extract_wikipedia_table_to_csv(url, output_file):

    response = requests.get(url)

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

        # Ask to choose a table
        table_choice = int(input("\nEnter the number of the table you want to extract: ")) - 1

        if table_choice < 0 or table_choice >= len(tables):
            print("Invalid table number. Exiting.")
            exit(1)
    else:
        table_choice = 0

    table_str = str(tables[table_choice])

    df = pd.read_html(StringIO(table_str))[0]

    df.to_csv(output_file, index=False)


# Soft Clean (choose a column)
def clean_date(input_file):

    df = pd.read_csv(input_file)

    print("Available columns:")
    for i, col in enumerate(df.columns, 1):
        print(f"{i}. {col}")

    # Find the country column
    country_col = find_country_column(df.columns)
    if not country_col:
        country_col = input('Enter the country column name: ')

    print(df.head())

    # Ask to choose a column to keep
    column_index = int(input('Enter the number of the column you want to keep: ')) - 1

    # Check if the column index is valid
    if column_index < 0 or column_index >= len(df.columns):
        print("Invalid column number. Please try again.")
        os.remove('tmp.csv')
        exit(1)

    column_to_keep = df.columns[column_index]

    result_df = df[[country_col, column_to_keep]]

    # Ask for an output file name
    output_file = input('Enter a file name: ')

    output_file += '.csv'

    result_df.to_csv(output_file, index=False)

    os.remove('tmp.csv')

url = input('Enter a URL: ')

output_file = 'tmp.csv'

extract_wikipedia_table_to_csv(url, output_file)
clean_date(output_file)


