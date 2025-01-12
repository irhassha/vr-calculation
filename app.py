import streamlit as st
import pandas as pd

# Fungsi untuk menghitung VR
def calculate_vr(discharge, load, CI, GCR, MB):
    try:
        vr = (discharge + load) / (((discharge + load) / CI / GCR) + MB)
        return round(vr, 2)
    except ZeroDivisionError:
        return 0

# Fungsi untuk menambahkan data baru ke DataFrame
def add_row_to_df(df, row_data):
    new_row = pd.DataFrame([row_data], columns=df.columns)
    return pd.concat([df, new_row], ignore_index=True)

# Input file Excel
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])
if uploaded_file is not None:
    # Membaca file Excel yang di-upload
    df = pd.read_excel(uploaded_file, engine="openpyxl")

    # Cek kolom yang diperlukan
    required_columns = ['Vessel', 'Month', 'Disch', 'Load', 'CI', 'GCR', 'MB']
    if not all(col in df.columns for col in required_columns):
        st.error("Data tidak lengkap! Kolom yang diperlukan: " + ", ".join(required_columns))
    else:
        # Hitung VR jika belum ada
        if 'VR' not in df.columns:
            df['VR'] = df.apply(lambda row: calculate_vr(
                row['Disch'], row['Load'], row['CI'], row['GCR'], row['MB']), axis=1)

        # Menampilkan tabel
        st.dataframe(df.style.format(precision=2), use_container_width=True)

        # Form untuk menambah data baru
        with st.form("add_data_form"):
            st.write("Tambah Data Kapal")
            new_data = {
                "Vessel": st.text_input("Vessel"),
                "Month": st.selectbox("Month", ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]),
                "Disch": st.number_input("Jumlah Bongkar", min_value=0, step=1),
                "Load": st.number_input("Jumlah Muat", min_value=0, step=1),
                "CI": st.number_input("Crane Intensity", min_value=0.1, step=0.1),
                "GCR": st.number_input("Performance Crane", min_value=0.1, step=0.1),
                "MB": st.number_input("Meal Break Time", min_value=0.0, step=0.1),
            }
            submit_button = st.form_submit_button("Tambah Data")

        if submit_button:
            if all(new_data.values()):
                # Tambah data baru
                df = add_row_to_df(df, new_data)
                df['VR'] = df.apply(lambda row: calculate_vr(
                    row['Disch'], row['Load'], row['CI'], row['GCR'], row['MB']), axis=1)
                st.success("Data berhasil ditambahkan!")
                st.dataframe(df.style.format(precision=2), use_container_width=True)
            else:
                st.error("Harap lengkapi semua input!")

        # Input untuk target VR dan estimasi kapal berikutnya
        target_vr = st.number_input("Masukkan target VR yang ingin dicapai", min_value=0.0, step=0.1, value=80.0)
        estimated_ships = st.number_input("Masukkan estimasi jumlah kapal berikutnya", min_value=1, step=1, value=5)

        # Hitung rate to go
        avg_vr = df['VR'].mean()
        total_ships = len(df) + estimated_ships
        total_vr_needed = total_ships * target_vr
        total_current_vr = len(df) * avg_vr
        vr_needed_by_new_ships = total_vr_needed - total_current_vr
        rate_to_go = vr_needed_by_new_ships / estimated_ships

        st.write(f"Rata-rata VR yang diperlukan oleh kapal berikutnya agar target tercapai: {round(rate_to_go, 2)}")
