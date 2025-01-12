import streamlit as st
import pandas as pd

# Fungsi untuk menghitung VR
def calculate_vr(discharge, load, CI, GCR, MB):
    try:
        vr = (discharge + load) / (((discharge + load) / CI / GCR) + MB)
        return round(vr, 2)
    except ZeroDivisionError:
        return 0

# Background color
st.markdown("""
    <style>
        body {
            background-color: #F0F8FF;
        }
    </style>
""", unsafe_allow_html=True)

# Input file excel
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])
if uploaded_file is not None:
    # Membaca file Excel yang di-upload
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    
    # Pastikan semua kolom yang dibutuhkan ada
    required_columns = ['Vessel', 'Month', 'Disch', 'Load', 'CI', 'GCR', 'MB']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Kolom berikut tidak ditemukan dalam data: {', '.join(missing_columns)}")
    else:
        # Menampilkan data awal
        st.write("Data Kapal:")
        st.dataframe(df)

        # Formulir untuk menambah data baru
        st.write("Tambah Data Baru:")
        with st.form(key="add_data_form"):
            new_data = {
                "Vessel": st.text_input("Vessel"),
                "Month": st.text_input("Month"),
                "Disch": st.number_input("Discharge", min_value=0, value=0),
                "Load": st.number_input("Load", min_value=0, value=0),
                "CI": st.number_input("Crane Intensity", min_value=0, value=1),
                "GCR": st.number_input("Performance Crane", min_value=0.1, value=1.0),
                "MB": st.number_input("Meal Break Time", min_value=0, value=0),
            }
            submit_button = st.form_submit_button("Tambahkan")

        if submit_button:
            # Tambahkan data baru ke dataframe
            new_data["VR"] = calculate_vr(new_data["Disch"], new_data["Load"], 
                                          new_data["CI"], new_data["GCR"], new_data["MB"])
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            st.success("Data baru berhasil ditambahkan!")
            st.write("Data terbaru:")
            st.dataframe(df)

        # Pilihan untuk rata-rata VR
        time_period = st.selectbox("Pilih periode perhitungan VR", ["Overall", "Per Month"])
        if time_period == "Per Month":
            month = st.selectbox("Pilih bulan", df['Month'].unique())
            avg_vr = df[df['Month'] == month]['VR'].mean()
            st.write(f"Rata-rata VR untuk bulan {month}: {round(avg_vr, 2)}")
        else:
            avg_vr = df['VR'].mean()
            st.write(f"Rata-rata VR keseluruhan: {round(avg_vr, 2)}")
        
        # Input untuk target VR dan estimasi jumlah kapal
        target_vr = st.number_input("Masukkan target VR yang ingin dicapai", min_value=0, value=80)
        estimated_ships = st.number_input("Masukkan estimasi jumlah kapal berikutnya", min_value=1, value=5)

        # Hitung total VR dan rata-rata VR yang diperlukan
        total_ships = len(df) + estimated_ships
        total_vr_needed = total_ships * target_vr
        total_current_vr = len(df) * avg_vr
        vr_needed_by_new_ships = total_vr_needed - total_current_vr
        avg_vr_for_new_ships = vr_needed_by_new_ships / estimated_ships

        # Menampilkan hasil Rate to Go
        st.write(f"Rata-rata VR yang diperlukan oleh kapal berikutnya agar target tercapai: {round(avg_vr_for_new_ships, 2)}")
