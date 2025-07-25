import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils.data_loader import load_sales_data

df = load_sales_data(sheet_name="Dane do panelu sprzedaży", worksheet_name="Obrót", 'asepta-4e6acac849fa.json')
today = datetime.today()
default_start = date(today.year, 1, 1)
default_end = today

def show1():
    st.title("📈 Twój Panel Sprzedażowy")
    with st.sidebar:
        st.title('Filtry:')
        name = st.text_input("Podaj nazwę klienta:")
        filter_mode = st.radio("Filtruj według:", ["Kategorii", "Produktów"])
        if filter_mode == "Kategorii":
            selected_groups = st.multiselect("Wybierz kategorie", ['Best Sellers', 'Nowa linia', 'Promocja'])
        else:
            selected_products = st.multiselect("Wybierz produkty", ['Pajęczak', 'Gardłosept', 'Oregasept'])
        date_range = st.date_input("Wybierz zakres dat", [default_start, default_end])
        st.text(date_range)
        col1, col2 = st.columns(2)
        with col1:
            search = st.button('Szukaj')
            
        with col2:
            st.button('Wyczyść')
    


    if st.button:
        col1, col2, col3 = st.columns(3)

    with col1:
        st.dataframe(df, hide_index=True)

    with col2:
        st.write('Pierwsza kolumna')

    with col3:
        st.write('Druga kolumna')








