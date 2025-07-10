#Łączy się z Google Sheets API
#Wczytuje dane jako pandas.DataFrame
#Czyści dane (np. konwersja dat, kolumny liczbowe)
#Zawiera ewentualne cache (@st.cache_data)

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
import streamlit as st

# Łączenie się z Google Sheets przez konto serwisowe
def load_sales_data(sheet_name: str, worksheet_name: str) -> pd.DataFrame: #, year=2025
    # Ścieżka do credentials
    cred_path = Path("credentials/google_credentials.json")

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_path, scope)
    client = gspread.authorize(creds)

    # Pobierz arkusz
    sheet = client.open(sheet_name)
    worksheet = sheet.worksheet(worksheet_name)

    # Wczytaj dane jako DataFrame
    data = worksheet.get("A2:N10")
    headers = worksheet.row_values(1)[:14]  
    df = pd.DataFrame(data, columns=headers)
    

    df.dropna(how='all', inplace=True)
    df['Rodzaj'] = df['Rodzaj '].str.strip()
    df.drop(columns='Rodzaj ', inplace=True)
    excluded_cols = ['Rodzaj', 'Kod produktu']
    cols_to_convert = df.columns.difference(excluded_cols)
    df[cols_to_convert] = df[cols_to_convert].fillna(0).astype(int)

    return df

def load_channel_data(sheet_name: str, worksheet_name: str) -> pd.DataFrame:
    # Ścieżka do credentials
    cred_path = Path("credentials/google_credentials.json")

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_path, scope)
    client = gspread.authorize(creds)

    # Pobierz arkusz
    sheet = client.open(sheet_name)
    worksheet = sheet.worksheet(worksheet_name)

    # Wczytaj dane jako DataFrame
    data = worksheet.get("A2:M5") #data = worksheet.get_all_records()  # Zwraca listę list (bez nagłówków)
    headers = worksheet.row_values(1)[:13]  # Pobierz nagłówki z pierwszego wiersza, kolumny A–E
    df = pd.DataFrame(data, columns=headers)

    df.dropna(how='all', inplace=True)

    # # Konwersja kolumn na odpowiednie typy
    # df['Data'] = pd.to_datetime(df['Data'], format="%Y-%m-%d")
    # df['Przychód'] = df['Przychód'].astype(float)

    # # Zmiana nazw kolumn
    # df.rename(columns={
    #     "Imię i nazwisko": "Sprzedawca",
    #     "Produkt": "Produkt",
    # }, inplace=True)

    return df
