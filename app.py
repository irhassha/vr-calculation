import streamlit as st
import pandas as pd

# Fungsi untuk menghitung VR
def calculate_vr(discharge, load, crane_intensity, crane_performance, meal_break):
    try:
        vr = (discharge + load) / (((discharge + load) / crane_intensity / crane_performance) + meal_break)
        return vr
    except ZeroDivisionError:
        return 0

# Input file excel
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    
    # Menghitung VR untuk setiap kapal
    df['VR'] = df.apply(lambda row: calculate_vr(
        row['Jumlah Bongkar'], row['Jumlah Muat'], row['Crane Intensity'],
        row['Performance crane per jam'], row['Total meal break']), axis=1)
    
    # Menampilkan data kapal dengan VR yang dihitung
    st.write("Data Kapal dengan VR yang dihitung:", df)
    
    # Memilih opsi apakah perhitungan VR berdasarkan bulan atau keseluruhan
    time_period = st.selectbox("Pilih periode perhitungan VR", ["Overall", "Per Month"])
    
    if time_period == "Per Month":
        # Menghitung rata-rata VR per bulan
        month = st.selectbox("Pilih bulan", df['Month'].unique())
        df_filtered = df[df['Month'] == month]
        avg_vr = df_filtered['VR'].mean()
        st.write(f"Rata-rata VR untuk bulan {month}: {avg_vr}")
    else:
        # Rata-rata VR keseluruhan
        avg_vr = df['VR'].mean()
        st.write(f"Rata-rata VR keseluruhan: {avg_vr}")
    
    # Menampilkan input untuk target VR dan estimasi jumlah kapal berikutnya
    target_vr = st.number_input("Masukkan target VR yang ingin dicapai", min_value=0, value=80)
    estimated_ships = st.number_input("Masukkan estimasi jumlah kapal berikutnya", min_value=1, value=5)
    
    # Menghitung total VR yang dibutuhkan untuk mencapai target rata-rata VR
    total_ships = len(df) + estimated_ships
    total_vr_needed = total_ships * target_vr
    
    # Menghitung total VR yang sudah ada
    total_current_vr = len(df) * avg_vr
    
    # Menghitung total VR yang perlu ditambahkan oleh kapal berikutnya
    vr_needed_by_new_ships = total_vr_needed - total_current_vr
    
    # Menghitung rata-rata VR yang diperlukan oleh kapal berikutnya
    average_vr_for_new_ships = vr_needed_by_new_ships / estimated_ships
    
    # Menampilkan hasil Rate to Go
    st.write(f"Rata-rata VR yang diperlukan oleh kapal berikutnya agar target tercapai: {average_vr_for_new_ships}")
