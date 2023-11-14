import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(layout="wide")

conn = st.experimental_connection("gsheets", type=GSheetsConnection)
data = conn.read(worksheet="db", usecols=list(range(4)))
data = data.dropna(how="all")

st.title("Monitoring Rekrutmen Mitra Statistik BPS Kabupaten Kepulauan Sula 2024")

st.header('Rekapan')

pendaftar_sula = data[data['wilayah']=='Kepulauan Sula']['posisi_daftar'].value_counts()
pendaftar_taliabu = data[data['wilayah']=='Pulau Taliabu']['posisi_daftar'].value_counts()

tab1, tab2 = st.tabs(["Kepulauan Sula", "Pulau Taliabu"])
with tab1:
    st.subheader(f"Tanggal Update: {data[data['wilayah']=='Kepulauan Sula']['date_update'].unique()[0]} WIT")
    st.subheader(f"Total pendaftar: {pendaftar_sula.sum()}")
    st.dataframe(pendaftar_sula)
with tab2:
    st.subheader(f"Tanggal Update: {data[data['wilayah']=='Pulau Taliabu']['date_update'].unique()[0]} WIT")
    st.subheader(f"Total pendaftar: {pendaftar_taliabu.sum()}")
    st.dataframe(pendaftar_taliabu)

st.markdown("---")

st.subheader('Daftar nama calon mitra yang berhasil mendaftar:')
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        posisi_daftar = st.multiselect(
            "Pilih posisi daftar:",
            options=data["posisi_daftar"].unique(),
            default=data["posisi_daftar"].unique()
        )
    with col2:
        wilayah = st.multiselect(
            "Pilih wilayah pendaftaran:",
            options=data["wilayah"].unique(),
            default=data["wilayah"].unique()
        )

    data_filtered = data.query(
        "posisi_daftar == @posisi_daftar & wilayah == @wilayah"
    )

    data_filtered = data_filtered.loc[:, data_filtered.columns != "date_update"]

    st.dataframe(data_filtered, use_container_width=True)
