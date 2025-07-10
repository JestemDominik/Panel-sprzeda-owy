import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from views.dashboard_rep import show1
from views.dashboard_management import show2
from pathlib import Path
from utils.data_loader import load_sales_data

# ------------------- ŁADOWANIE KONFIGURACJI -------------------
def load_authenticator(config_path=Path("credentials/credentials.yaml")):
    with open(config_path) as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    return authenticator, config


# ------------------- GŁÓWNA APLIKACJA -------------------
st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")
#df = load_sales_data(sheet_name="Agenci AI", worksheet_name="Dane sprzedażowe")

authenticator, config = load_authenticator()

name, auth_status, username = authenticator.login("Zaloguj się", "main")

if auth_status == False:
    st.error("Niepoprawny login lub hasło.")
elif auth_status == None:
    st.warning("Wprowadź dane logowania.")
elif auth_status:

    role = config['credentials']['usernames'][username].get("role")

    if role == "rep":
        show1()
    elif role == "management":
        show2()

    authenticator.logout("Wyloguj się", "main")