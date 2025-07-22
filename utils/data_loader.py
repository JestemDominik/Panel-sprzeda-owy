import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
import streamlit as st

def load_sales_data(sheet_name: str, worksheet_name: str) -> pd.DataFrame:
    
    credentials_dict = {
            "type": "service_account",
            "project_id": "asepta",
            "private_key_id": "abc969b773623cb34a9ded94a8d0f99d61f6a8ac",
            "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQD0VAxsVbnd2y6w
rn5FLs7rARlccSDGofvUixJUPs3GwBgiNV44ec+6HLdO8YS++X4ajXulxiCDC+5w
DP6b4gGdJRiSt5626GN+/B0zJq3hLeOWvCJIB5ABLd79Bnwa3HmxFB1WsCZGvNB7
nbemi1AoS37bQwjihjlvsPC6NN+pzMCT8gkBok+d70YS7P5/J24n3bKKRM9gJa8d/
sCPoba/v2DGsvCJK5gT89hDey4HBERWrXOnIHdMlHOPbg/PY6VIXpsXxsdaDdLOs
YCNuhNbvpIdk7RyVd8jAZxjh46/o5lpTbOtqAwwld8V7n0RkAG31rKI0njfMSLLM
XidEt477AgMBAAECggEATquZbHCV7leayw0EX2ZY/dZWwisy8IJLwf4dor6uJ2bG
3ozsj6a5OiXw6BxgL9XJwub3f0MySL/YwH+Oo8a72kuNhABXvHFLSCIJjOTRbAYI
mApvx12YAqkweaxS3ZtMG7ZsU/NX/8LgJj4X0nQP4k/iX4mKDor2EjS2kIYGmZuv
2BnXNV+/KkiPMGMClWojHtUzTrR/pBPZoF7c79yQP1KtFFjd4iHZZbmSye3or7TV
+ruQhOwpDXfxy8rS2yF/CFrE4zhok9CxdzUDMLW6sIjh0si/P8xZp0e5+samUGSd
fhCRHnEbC8nc6Dd2tJiOKfR5WQbwP2c6zp0T0D/kYQKBgQD+gfQAeZfxUHpsd0lj
RH6jlkNtKDqRdwepckgJHTYfNqOYO0mx5/OiCiwOjYcLP2gYgFJIfAazQ/ZGXoKx
HjfnrpNDoh0RfjqIu90wCiT7Qk1qojvLbSwqQNvKLTRgd3jCafY/Vld/qVSBxmL9
AIcmTrTdS0AqBgUBLfkJ/UvLqQKBgQD1wtCkWAHyswXYE/3FPQadJEfsjJHvVshm
f9NU618pUMQP7oYjSl8dfQEUfx3Be/CX2cQCXjTlSeHvbZDqJS30yOTDYndjsspA
MfezMf47DVrFkB8VOI54e3/v4SbExEyxq89vvxxIByFKbYiTO/t9oaWAX9c1UbX4
cdM3FC5MAwKBgQCtlr1yRX0ZHqchrArmJiWqNicvIK0x4lnbfRMdBEuR5paWknml
WmuWLhH2qxlc1paNf5ifz9hSFRy4ymWhoNbIsw3Gp5/j+pC6CkjHJ2Qp7AMZpCXc
jk39U9eVglejJFm9YMCQWre7XydAjKufnOiRfEVoWpcdEpX/Q/gElDtKYQKBgQCZ
GIVU+6YrBK7tTnbV+hA2sDVF/MOkb1Fj2NlTm1Sqri+VJSfWsCvUeNzFYfKtZ4IX
docOWpVlCMOAnaaa1hJs3QD1Xk+1gdlQaFBABzKyor0bOY7Db3oBQB4Q1xeJmCeW
vsr4d/ssO5TXgqiD3+fo+VvaPtoX0xEi9fV36FB29QKBgQCVR6+CnQQ2HhUCEl9N
zCKKLZSEduIMKJgLJwnD1NEtj/9GIQx7hpOmD97K1zIiqIGOgi6jNMZZzftlIBdn
GIMJvlH4TfjCOjLC+yc2emTeY93NT6JvUEzzf08RTmNYWi41P58iaBKL3aQPW1D2
IaDu9D32FHnyUuNweND+9uRB6w==
-----END PRIVATE KEY-----""",
            "client_email": "python-api@asepta.iam.gserviceaccount.com",
            "client_id": "115844564356560844548",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/python-api@asepta.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
        }

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    client = gspread.authorize(creds)

    sheet = client.open(sheet_name)
    worksheet = sheet.worksheet(worksheet_name)

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

    credentials_dict = {
        "type": "service_account",
        "project_id": "asepta",
        "private_key_id": "abc969b773623cb34a9ded94a8d0f99d61f6a8ac",
        "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQD0VAxsVbnd2y6w
rn5FLs7rARlccSDGofvUixJUPs3GwBgiNV44ec+6HLdO8YS++X4ajXulxiCDC+5w
DP6b4gGdJRiSt5626GN+/B0zJq3hLeOWvCJIB5ABLd79Bnwa3HmxFB1WsCZGvNB7
nbemi1AoS37bQwjihjlvsPC6NN+pzMCT8gkBok+d70YS7P5/J24n3bKKRM9gJa8d/
sCPoba/v2DGsvCJK5gT89hDey4HBERWrXOnIHdMlHOPbg/PY6VIXpsXxsdaDdLOs
YCNuhNbvpIdk7RyVd8jAZxjh46/o5lpTbOtqAwwld8V7n0RkAG31rKI0njfMSLLM
XidEt477AgMBAAECggEATquZbHCV7leayw0EX2ZY/dZWwisy8IJLwf4dor6uJ2bG
3ozsj6a5OiXw6BxgL9XJwub3f0MySL/YwH+Oo8a72kuNhABXvHFLSCIJjOTRbAYI
mApvx12YAqkweaxS3ZtMG7ZsU/NX/8LgJj4X0nQP4k/iX4mKDor2EjS2kIYGmZuv
2BnXNV+/KkiPMGMClWojHtUzTrR/pBPZoF7c79yQP1KtFFjd4iHZZbmSye3or7TV
+ruQhOwpDXfxy8rS2yF/CFrE4zhok9CxdzUDMLW6sIjh0si/P8xZp0e5+samUGSd
fhCRHnEbC8nc6Dd2tJiOKfR5WQbwP2c6zp0T0D/kYQKBgQD+gfQAeZfxUHpsd0lj
RH6jlkNtKDqRdwepckgJHTYfNqOYO0mx5/OiCiwOjYcLP2gYgFJIfAazQ/ZGXoKx
HjfnrpNDoh0RfjqIu90wCiT7Qk1qojvLbSwqQNvKLTRgd3jCafY/Vld/qVSBxmL9
AIcmTrTdS0AqBgUBLfkJ/UvLqQKBgQD1wtCkWAHyswXYE/3FPQadJEfsjJHvVshm
f9NU618pUMQP7oYjSl8dfQEUfx3Be/CX2cQCXjTlSeHvbZDqJS30yOTDYndjsspA
MfezMf47DVrFkB8VOI54e3/v4SbExEyxq89vvxxIByFKbYiTO/t9oaWAX9c1UbX4
cdM3FC5MAwKBgQCtlr1yRX0ZHqchrArmJiWqNicvIK0x4lnbfRMdBEuR5paWknml
WmuWLhH2qxlc1paNf5ifz9hSFRy4ymWhoNbIsw3Gp5/j+pC6CkjHJ2Qp7AMZpCXc
jk39U9eVglejJFm9YMCQWre7XydAjKufnOiRfEVoWpcdEpX/Q/gElDtKYQKBgQCZ
GIVU+6YrBK7tTnbV+hA2sDVF/MOkb1Fj2NlTm1Sqri+VJSfWsCvUeNzFYfKtZ4IX
docOWpVlCMOAnaaa1hJs3QD1Xk+1gdlQaFBABzKyor0bOY7Db3oBQB4Q1xeJmCeW
vsr4d/ssO5TXgqiD3+fo+VvaPtoX0xEi9fV36FB29QKBgQCVR6+CnQQ2HhUCEl9N
zCKKLZSEduIMKJgLJwnD1NEtj/9GIQx7hpOmD97K1zIiqIGOgi6jNMZZzftlIBdn
GIMJvlH4TfjCOjLC+yc2emTeY93NT6JvUEzzf08RTmNYWi41P58iaBKL3aQPW1D2
IaDu9D32FHnyUuNweND+9uRB6w==
-----END PRIVATE KEY-----""",
        "client_email": "python-api@asepta.iam.gserviceaccount.com",
        "client_id": "115844564356560844548",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/python-api@asepta.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    client = gspread.authorize(creds)

    sheet = client.open(sheet_name)
    worksheet = sheet.worksheet(worksheet_name)

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
