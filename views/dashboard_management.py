import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import plotly.graph_objects as go
from utils.data_loader import load_sales_data, load_channel_data
import plotly.express as px
import matplotlib.pyplot as plt
import base64

# if 'year' not in st.session_state:
#     st.session_state["year"] = 2025


# SKUP SIĘ NA TYM CO KLIENT CHCE ZOBACZYĆ
# --- ŁADOWANIE DANYCH ---
df = load_sales_data(sheet_name="Dane do panelu sprzedaży", worksheet_name="Obrót", 'asepta-4e6acac849fa.json') #Produkty , year=st.session_state['year']
df1 = load_channel_data(sheet_name="Dane do panelu sprzedaży", worksheet_name="Kanał", 'asepta-4e6acac849fa.json') # Kanały
df2 = load_channel_data(sheet_name="Dane do panelu sprzedaży", worksheet_name="Grupy klientów", 'asepta-4e6acac849fa.json')

# --- ŁADOWANIE OBRAZÓW ---
def get_image_base64(path):
    with open(path, "rb") as file:
        data = file.read()
    return base64.b64encode(data).decode()
image_logo = get_image_base64("images/logo_asepta.png")
image_line = get_image_base64("images/line_photo.png")


# --- WSTĘPNE PRZETWARZANIE DANYCH ---   PRZYSZŁOŚCIOWO WRZUCIĆ DO FUNKCJI

# --- Sprzedaż --- 
# (dołączona do funkcji)

# --- Kanały ---
excluded_cols = ['Kanał']
cols_to_convert = df1.columns.difference(excluded_cols)
df1[cols_to_convert] = df1[cols_to_convert].fillna(0).astype(int)

# --- Klienci ---
excluded_cols = ['Klient']
cols_to_convert = df2.columns.difference(excluded_cols)
df2[cols_to_convert] = df2[cols_to_convert].fillna(0).astype(int)

# --- OBLICZENIA PODSTAWOWE ---

# Suma roczna dla każdego wiersza
months = ['Sty', 'Lut', 'Mar', 'kwi', 'maj', 'cze', 'lip', 'sie', 'wrz', 'paź', 'lis', 'gru']
miesiace_order = [m.capitalize() for m in months]

# Sumy roczne
df['Obrót'] = df[months].sum(axis=1)
df1['Obrót'] = df1[months].sum(axis=1)
df2['Obrót'] = df2[months].sum(axis=1)

# Udział w rynku według rodzaju
df_grouped = df.groupby('Rodzaj')['Obrót'].sum().reset_index()
laczny_obrot1 = df["Obrót"].sum()
df_grouped["udział w rynku %"] = round((df_grouped['Obrót'] / laczny_obrot1) * 100, 1)
df_grouped.sort_values('udział w rynku %', ascending=False, inplace=True)
df_grouped_display = df_grouped[["Rodzaj", "Obrót", "udział w rynku %"]].reset_index(drop=True)

# Top produkty
top_products = (
    df.groupby(['Kod produktu', 'Rodzaj'])['Obrót']
    .sum()
    .reset_index()
    .sort_values('Obrót', ascending=False)
    .head(8)
)

# --- TRANSFORMACJE DLA WYKRESÓW LINIOWYCH ---

# Kategorie
df_long = df.melt(id_vars=['Rodzaj'], value_vars=months, var_name='Miesiąc', value_name='Obrót_miesięczny')
df_long['Miesiąc'] = pd.Categorical(df_long['Miesiąc'].str.capitalize(), categories=miesiace_order, ordered=True)
df_grouped1 = df_long.groupby(['Rodzaj', 'Miesiąc']).sum().reset_index()
df_grouped1 = df_grouped1[df_grouped1['Obrót_miesięczny'] > 0]

#Produkty
df_long1 = df.melt(id_vars=['Kod produktu'], value_vars=months, var_name='Miesiąc', value_name='Obrót_miesięczny')
df_long1['Miesiąc'] = pd.Categorical(df_long1['Miesiąc'].str.capitalize(), categories=miesiace_order, ordered=True)
df_grouped2 = df_long1.groupby(['Kod produktu', 'Miesiąc']).sum().reset_index()
df_grouped2 = df_grouped2[df_grouped2['Obrót_miesięczny'] > 0]

#Kanały
df_long2 = df1.melt(id_vars=['Kanał'], value_vars=months, var_name='Miesiąc', value_name='Obrót_miesięczny')
df_long2['Miesiąc'] = pd.Categorical(df_long2['Miesiąc'].str.capitalize(), categories=miesiace_order, ordered=True)
df_long2['Obrót_miesięczny'] = pd.to_numeric(df_long2['Obrót_miesięczny'], errors='coerce').fillna(0).astype(int)
df_grouped3 = df_long2.groupby(['Kanał', 'Miesiąc']).sum().reset_index()
df_grouped3 = df_grouped3[df_grouped3['Obrót_miesięczny'] > 0]

#Klienci
df_long3 = df2.melt(id_vars=['Klient'], value_vars=months, var_name='Miesiąc', value_name='Obrót_miesięczny')
df_long3['Miesiąc'] = pd.Categorical(df_long3['Miesiąc'].str.capitalize(), categories=miesiace_order, ordered=True)
df_long3['Obrót_miesięczny'] = pd.to_numeric(df_long3['Obrót_miesięczny'], errors='coerce').fillna(0).astype(int)
df_grouped4 = df_long3.groupby(['Klient', 'Miesiąc']).sum().reset_index()
df_grouped4 = df_grouped4[df_grouped4['Obrót_miesięczny'] > 0]
# --- OBLICZANIE DYNAMIKI ---

#Produkty
suma_po_mies = df[months].sum()
niezerowe_mies = suma_po_mies[suma_po_mies > 0].index.tolist()
ostatni = niezerowe_mies[-1]
poprzedni = niezerowe_mies[-2]
df_diff = df[["Kod produktu", ostatni, poprzedni]].copy()
df_diff["Różnica"] = df_diff["cze"] - df_diff["maj"]
top_wzrost = df_diff.loc[df_diff["Różnica"].abs().nlargest(5).index]

# Kanały
suma_po_mies1 = df1[months].sum()
niezerowe_mies1 = suma_po_mies1[suma_po_mies1 > 0].index.tolist()
ostatni1 = niezerowe_mies1[-1]
poprzedni1 = niezerowe_mies1[-2]
df_diff1 = df1[["Kanał", ostatni1, poprzedni1]].copy()
df_diff1["Różnica"] = df_diff1["cze"] - df_diff1["maj"]
top_wzrost1 = df_diff1.loc[df_diff1["Różnica"].abs().nlargest(5).index]

# Klienci
suma_po_mies2 = df2[months].sum()
niezerowe_mies2 = suma_po_mies2[suma_po_mies2 > 0].index.tolist()
ostatni2 = niezerowe_mies2[-1]
poprzedni2 = niezerowe_mies1[-2]
df_diff2 = df2[["Klient", ostatni2, poprzedni2]].copy()
df_diff2["Różnica"] = df_diff2["cze"] - df_diff2["maj"]
top_wzrost2 = df_diff2.loc[df_diff2["Różnica"].abs().nlargest(5).index]

# --- WYKRES 1: Udział w rynku wg kategorii ---

fig1 = px.bar(
    df_grouped,
    y="Rodzaj",
    x="udział w rynku %",
    orientation="h",
    text="udział w rynku %",
    color="Rodzaj",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig1.update_layout(
    yaxis_title="",
    xaxis_title="Udział w rynku (%)",
    showlegend=False,
    height=300
)

# --- WYKRES 2 V1: Obrót miesięczny wg rodzaju ---
fig2 = px.line(
    df_grouped1,
    x='Miesiąc',
    y='Obrót_miesięczny',
    color='Rodzaj',
    markers=True,
    line_shape='linear'
)
fig2.update_layout(
    title="Obroty miesięczne według rodzaju",
    xaxis_title="Miesiąc",
    yaxis_title="Suma obrotu",
    template="simple_white"
)

# --- WYKRES 2 V2: Obrót miesięczny wg rodzaju ---
fig4 = px.line(
    df_grouped2,
    x='Miesiąc',
    y='Obrót_miesięczny',
    color='Kod produktu',
    markers=True,
    line_shape='linear'
)
fig4.update_layout(
    title="Obroty miesięczne według rodzaju",
    xaxis_title="Miesiąc",
    yaxis_title="Suma obrotu",
    template="simple_white"
)

#--- WYKRES 2 V3: Obrót miesięczny wg kanału ---
fig5 = px.line(
    df_grouped3,
    x='Miesiąc',
    y='Obrót_miesięczny',
    color='Kanał',
    markers=True,
    line_shape='linear'
)
fig5.update_layout(
    title="Obroty miesięczne według rodzaju",
    xaxis_title="Miesiąc",
    yaxis_title="Suma obrotu",
    template="simple_white"
)
#--- WYKRES 2 V4: Obrót miesięczny wg klienta ---
fig9 = px.line(
    df_grouped4,
    x='Miesiąc',
    y='Obrót_miesięczny',
    color='Klient',
    markers=True,
    line_shape='linear'
)
fig9.update_layout(
    title="Obroty miesięczne według rodzaju",
    xaxis_title="Miesiąc",
    yaxis_title="Suma obrotu",
    template="simple_white"
)

# --- WYKRES 3: Donut chart – realizacja celu ---
current_value = laczny_obrot1
yearly_goal = 300
completion_percent = round((current_value / yearly_goal) * 100, 1)
remaining_percent = 100 - completion_percent

fig = go.Figure(data=[go.Pie(
    labels=["Zrealizowano", "Pozostało"],
    values=[completion_percent, remaining_percent],
    hole=0.6,
    marker=dict(colors=["#307c34", "#e8e8e8"]),
    textinfo="none"
)])
fig.update_layout(
    annotations=[dict(text=f"{completion_percent}%", x=0.5, y=0.5, font_size=24, showarrow=False)],
    showlegend=False,
    margin=dict(t=20, b=20, l=20, r=20),
    width=400,
    height=400
)

# --- WYKRES 4: TOP 10 produktów ---
fig3 = px.bar(
    top_products, 
    y="Kod produktu",
    x='Obrót',
    orientation="h",
    color="Rodzaj",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig3.update_layout(
    yaxis={'categoryorder':'total ascending'},
    title="Topowe produkty",
    xaxis_title="Obroty miesięczne według rodzaju",
    showlegend=False,
    height=420
)
# --- WYKRES 5 V1: Dynamika miesięczna produktów ---
fig6 = px.bar(
    top_wzrost,
    x="Kod produktu",
    y="Różnica",
    #orientation="h",
    #color="Rodzaj produktu",
    title="Top dynamika cen",
    text="Różnica",
    color_discrete_sequence=["#307c34"]
)
fig6.update_traces(textposition="outside")
fig6.update_layout(yaxis_title="Wzrost sprzedaży", xaxis_title="Kanał")

# --- WYKRES 5 V2: Dynamika miesięczna kanałów ---

fig7 = px.bar(
    top_wzrost1,
    x="Kanał",
    y="Różnica",
    #orientation="h",
    #color="Rodzaj produktu",
    title="Top dynamika Kanałów",
    text="Różnica",
    color_discrete_sequence=["#307c34"]
)
fig7.update_traces(textposition="outside")
fig7.update_layout(yaxis_title="Wzrost sprzedaży", xaxis_title="Produkt")

# --- WYKRES 5 V3: Dynamika miesięczna Klientów ---

figb = px.bar(
    top_wzrost2,
    x="Klient",
    y="Różnica",
    #orientation="h",
    #color="Rodzaj produktu",
    title="Top dynamika Klientów",
    text="Różnica",
    color_discrete_sequence=["#307c34"]
)
figb.update_traces(textposition="outside")
figb.update_layout(yaxis_title="Wzrost sprzedaży", xaxis_title="Produkt")

# --- WYKRES 6 V1: Histogram dla kanałów ---

fig8 = px.bar(
    df1,
    x="Kanał",
    y="Obrót",
    #orientation="h",
    #color="Rodzaj produktu",
    #title="Top dynamika cen",
    #text="Różnica",
    color_discrete_sequence=["#307c34"]
)
fig8.update_layout(
    yaxis={'categoryorder':'total ascending'},
    title="Topowe produkty",
    xaxis_title="Obroty miesięczne według rodzaju",
    showlegend=False,
    height=420
)
# --- WYKRES 6 V2: Histogram dla klientów ---
figa = px.bar(
    df2,
    x="Klient",
    y="Obrót",
    #orientation="h",
    #color="Rodzaj produktu",
    #title="Top dynamika cen",
    #text="Różnica",
    color_discrete_sequence=["#307c34"]
)
figa.update_layout(
    yaxis={'categoryorder':'total ascending'},
    title="Klienci",
    xaxis_title="Klienci",
    showlegend=False,
    height=420
)

#--- FUNKCJA WYŚWIETLANIA PANELU ---
def show2():
    st.title("📊 Panel Sprzedażowy Asepta")
    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col1:
        st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #307c34, #215624);
                    padding: 30px; border-radius: 20px; color: white;
                    text-align: center; font-size: 28px; font-weight: bold;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
            Całkowity obrót<br>
            <span style="font-size: 48px;">{laczny_obrot1:,.0f} zł</span>
        </div>
        """,
        unsafe_allow_html=True
        )
        st.plotly_chart(fig, use_container_width=False)

        tcol1, tcol2 = st.columns(2)
        with tcol1:
            st.write("####")
            st.markdown("**Udział Kategorii w rynku**")
            st.dataframe(df_grouped_display)

        with tcol2:
            st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/jpeg;base64,{image_logo}" style="width:40%;"/>
        </div>
        """,
        unsafe_allow_html=True
        )
        
        acol1, acol2 = st.columns(2)
        with acol1:
            category = st.selectbox('Wybierz co ma pokazać wykres:', ["Produkty", "Kategorie"])
        with acol1:
            year = st.selectbox('Wybierz rok:', [2025, 2024, 2023])
            # if year != st.session_state["year"]:
            #     st.session_state["year"] = year
            #     st.rerun
        
        if category == "Produkty":
            st.plotly_chart(fig4, width=150)
        else:
            st.plotly_chart(fig2, width=150)

    with col3:
        #st.subheader('TOP 10 PRODUKTÓW')
        st.plotly_chart(fig3, use_container_width=True)
        st.plotly_chart(fig6, use_container_width=True)
    
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/jpeg;base64,{image_line}" style="width:100%;"/>
        </div>
        """,
        unsafe_allow_html=True
        )
    
    st.subheader("KANAŁY SPRZEDAŻY 👨‍💼")
    col1, col2, col3 = st.columns([1.5, 1, 1])

    with col1:
        st.plotly_chart(fig5, width=150)
    
    with col2:
        #st.table(df1)
        st.plotly_chart(fig8, width=150)

    with col3:
        st.plotly_chart(fig7, width=150)

    st.subheader("KLIENCI 👨‍🌾")
    col1, col2, col3 = st.columns([1.5, 1, 1])

    with col1:
        st.plotly_chart(fig9, use_container_width=True)

    with col2:
        st.plotly_chart(figa, width=150)

    with col3:
        st.plotly_chart(figb, width=150)
