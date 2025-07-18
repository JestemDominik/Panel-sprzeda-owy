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
def load_authenticator():
    # Budowanie struktury z secrets
    creds = {
        'usernames': {
            "rwasikiewicz": {
                "name": st.secrets["auth.credentials.usernames.rwasikiewicz"]["name"],
                "password": st.secrets["auth.credentials.usernames.rwasikiewicz"]["password"],
                "role": st.secrets["auth.credentials.usernames.rwasikiewicz"]["role"],
            },
            "dwasikiewicz": {
                "name": st.secrets["auth.credentials.usernames.dwasikiewicz"]["name"],
                "password": st.secrets["auth.credentials.usernames.dwasikiewicz"]["password"],
                "role": st.secrets["auth.credentials.usernames.dwasikiewicz"]["role"],
            },
        }
    }

    config = {
        "credentials": creds,
        "cookie": {
            "name": st.secrets["auth_cookie_name"],
            "key": st.secrets["auth_cookie_key"],
            "expiry_days": st.secrets["auth_cookie_expiry_days"]
        },
        "preauthorized": {
            "emails": st.secrets["auth_preauthorized_emails"]
        }
    }

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["preauthorized"]
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
