import streamlit as st
import pandas as pd
import numpy as np

st.title("Mapa interactivo e histograma de crímenes en la ciudad de Nueva York")
st.subheader("Actividad 4.2 Aplicación Móvil")


# Utilizamos cache para solo tener que cargar los datos una sola vez
@st.cache
def load_data(
    DATA_URL,
    DATE_COLUMN="date/time",
):
    data = pd.read_csv(DATA_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN], errors="coerce")
    return data


data_load_state = st.text("Cargando datos...")
data = load_data("NYPD_Complaint_Data_Historic.zip", "cmplnt_fr_dt")

# Mostramos el número de crímenes por mes
st.subheader("Número de crímenes por mes")
hist_values = np.histogram(data["cmplnt_fr_dt"].dt.month, bins=12, range=(0, 13))[0]
st.bar_chart(hist_values)

# Generamos una lista única de tipos de crímenes
ofensas = list(set(data["ofns_desc"].dropna()))
options = st.selectbox(
    "Filtrar con base en el tipo de crímen",
    ofensas,
)

# Filtramos el conjunto completo de datos utilizando la seleccion de arriba
st.subheader(f"Map of crimes of {options}")
subset_clean = data[["latitude", "longitude", "ofns_desc"]].dropna()
mask = subset_clean["ofns_desc"] == options

# Generamos un mapa con la ubicación geográfica del lugar del crímen
st.map(subset_clean[mask])

st.subheader("Referencias")

st.text(
    "Create a data explorer app — Streamlit 0.76.0 documentation. (2021). Retrieved 1 August 2021, from https://docs.streamlit.io/en/0.76.0/tutorial/create_a_data_explorer_app.html"
)

st.text(
    "New York City Crimes. (2021). Retrieved 1 August 2021, from https://www.kaggle.com/adamschroeder/crimes-new-york-city/version/1?select=Crime_Column_Description.csv"
)
