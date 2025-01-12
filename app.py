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
    
    # Menampilkan data di editor untuk memungkinkan pengguna menambah/mengubah data
    st.write("Edit data di bawah ini jika diperlukan:")
    df = st.experimental_data_editor(df, num_rows="dynamic")

    # Pastikan semua kolom yang dibutuhkan ada
    required_columns = ['Vessel', 'Month', 'Disch', 'Load', 'CI', 'GCR', 'MB']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Kolom berikut tidak ditemukan dalam data: {', '.join(missing_columns)}")
    else:
        # Menghitung VR untuk setiap kapal jika kolom VR belum ada
        if 'VR' not in df.columns:
            df['VR'] = df.apply(lambda row: calculate_vr(
                row['Disch'], row['Load'], row['CI'], row['GCR'], row['MB']), axis=1)
        else:
            # Update kolom VR jika data diubah
            df['VR'] = df.apply(lambda row: calculate_vr(
                row['Disch'], row['Load'], row['CI'], row['GCR'], row['MB']), axis=1)
        
        # Menampilkan data kapal dengan VR yang dihitung
        st.write("Data Kapal dengan VR yang dihitung:", df)

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
