import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(
    page_title="Monitoring Mitra 8203",
    page_icon=":bookmark_tabs:",
    layout="wide"
)

@st.cache_data(ttl=60)
def load_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(worksheet="db", usecols=list(range(5)))
    data = data.dropna(how="all")
    return data

st.markdown("""
<style>
p {
    margin: 0px;
    padding: 0px;
    font-size: 20px
}
.big-font {
    font-size:42px !important;
}
.small-font {
    font-size:16px;
}
</style>
""", unsafe_allow_html=True)

data = load_data()

def main():

    st.title("Monitoring Mitra Statistik BPS Kabupaten Kepulauan Sula 2024")
    st.markdown("---")

    date_sula = data[data['wilayah']=='Kepulauan Sula']['date_update'].unique()[0]
    date_taliabu = data[data['wilayah']=='Pulau Taliabu']['date_update'].unique()[0]

    progress_sula = round(len(data[(data['wilayah']=='Kepulauan Sula') & (data['status_pi']=='Disetujui')])/len(data[(data['wilayah']=='Kepulauan Sula')]),2)
    progress_taliabu = round(len(data[(data['wilayah']=='Pulau Taliabu') & (data['status_pi']=='Disetujui')])/len(data[(data['wilayah']=='Pulau Taliabu')]),2)

    st.subheader("Progress persetujuan Pakta Integritas:")

    col1,col2 = st.columns(2)
    with col1:
        st.markdown(f'''<p>Kepulauan Sula</p>  
                    <p class="big-font">{progress_sula}%</p>  
                    <p class="small-font">Updated at {date_sula}</p>''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''<p>Pulau Taliabu</p>  
                    <p class="big-font">{progress_taliabu}%</p>  
                    <p class="small-font">Updated at {date_taliabu}</p>''', unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("Daftar Mitra BPS Kabupaten Kepulauan Sula:")

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            status_pi = st.multiselect(
                "Pilih Status Pakta Integritas:",
                options=data["status_pi"].dropna().unique(),
                default=data["status_pi"].dropna().unique()
            )
        with col2:
            wilayah = st.multiselect(
                "Pilih wilayah pendaftaran:",
                options=data["wilayah"].dropna().unique(),
                default=data["wilayah"].dropna().unique()
            )
            
        search_name = st.text_input("Search nama:")

        data_filtered = data.query(
            "status_pi == @status_pi & wilayah == @wilayah"
        )

        data_filtered = data_filtered.loc[:, data_filtered.columns != "date_update"]

        if search_name is not None:
            data_filtered = data_filtered[data_filtered['nama'].str.contains(search_name, case=False)]


        st.data_editor(
            data_filtered,
            column_config= {
                "nama": "Nama",
                "jenis_mitra" : "Jenis Mitra",
                "status_pi" : "Status Pakta Integritas",
                "wilayah" : "Wilayah Domisili"
            },
            disabled= ["nama", "jenis_mitra", "status_pi", "wilayah"],
            use_container_width=True,
            hide_index=True)

if __name__ == "__main__":
    main()
