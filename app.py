import streamlit as st
import pandas as pd
from io import BytesIO

# Fungsi untuk menghitung VR dengan pengecekan pembagian nol
def calculate_vr(discharge, load, crane_intensity, crane_performance, meal_break):
    if crane_intensity == 0 or crane_performance == 0 or (discharge + load) == 0:
        return 0  # Atau bisa mengembalikan nilai lainnya jika ingin menghindari pembagian dengan nol
    vr = (discharge + load) / (((discharge + load) / crane_intensity / crane_performance) + meal_break)
    return vr

# Fungsi untuk menghitung rate to go
def calculate_rate_to_go(df, target_vr):
    # Menghitung rata-rata VR yang sudah ada
    avg_vr = df['VR'].mean()
    if avg_vr == 0:
        return target_vr  # Jika avg_vr adalah 0, kapal berikutnya butuh target VR penuh
    return target_vr - avg_vr

# Upload file Excel untuk data kapal
st.title('Kalkulator VR Kapal')

# Upload file Excel
uploaded_file = st.file_uploader("Unggah Data Kapal (Excel)", type=["xlsx"])

# Inisialisasi df sebagai None
df = None

# Jika file di-upload, load data dan tampilkan
if uploaded_file is not None:
    # Membaca file Excel
    df = pd.read_excel(uploaded_file)
    st.write("Data Kapal yang Diupload:")
    st.write(df)

    # Memastikan kolom yang dibutuhkan ada
    required_columns = ['Vessel', 'Month', 'Jumlah Bongkar', 'Jumlah Muat', 'Crane Intensity', 'Performance Crane', 'Meal Break Time']
    for col in required_columns:
        if col not in df.columns:
            st.error(f"Kolom '{col}' tidak ditemukan dalam file Excel.")
            df = None
            break

else:
    st.info("Silakan unggah file Excel dengan data kapal.")

# Menambahkan baris baru jika ada tombol tambah
if df is not None and st.button("Tambah Data Kapal"):
    new_row = {
        'Vessel': '',
        'Month': '',
        'Jumlah Bongkar': 0,
        'Jumlah Muat': 0,
        'Crane Intensity': 0,
        'Performance Crane': 0,
        'Meal Break Time': 0
    }
    # Menambahkan baris baru ke DataFrame menggunakan pd.concat
    new_df = pd.DataFrame([new_row])
    df = pd.concat([df, new_df], ignore_index=True)

# Menampilkan tabel yang bisa diedit hanya jika df ada
if df is not None:
    # Menampilkan data tanpa kolom nomor paling kiri
    df = df[['Vessel', 'Month', 'Jumlah Bongkar', 'Jumlah Muat', 'Crane Intensity', 'Performance Crane', 'Meal Break Time']]
    
    st.write("Tabel Data Kapal:")
    st.write(df)

    # Menghitung VR untuk kapal yang ada
    df['VR'] = df.apply(lambda row: calculate_vr(row['Jumlah Bongkar'], row['Jumlah Muat'], row['Crane Intensity'], 
                                                 row['Performance Crane'], row['Meal Break Time']), axis=1)

    # Menampilkan data kapal dengan VR
    st.write("Data Kapal dan VR:")
    st.write(df[['Vessel', 'Month', 'VR']])

    # Pilihan untuk menghitung rata-rata VR per bulan atau keseluruhan
    avg_option = st.selectbox("Pilih Opsi Rata-rata VR", ["Per Bulan", "Secara Keseluruhan"])

    # Menghitung rata-rata VR berdasarkan pilihan
    if avg_option == "Per Bulan":
        avg_vr_per_month = df.groupby('Month')['VR'].mean()
        st.write("Rata-rata VR per Bulan:")
        st.write(avg_vr_per_month)
    else:
        overall_avg_vr = df['VR'].mean()
        st.write(f"Rata-rata VR Secara Keseluruhan: {overall_avg_vr:.2f}")

    # Kolom untuk menginput target VR
    target_vr = st.number_input("Masukkan Target VR", min_value=0.0, step=0.01)

    # Menampilkan hasil perhitungan target VR
    st.write(f"Target VR yang dimasukkan: {target_vr}")

    # Menghitung rate to go untuk kapal berikutnya
    df['Rate to Go'] = df.apply(lambda row: calculate_rate_to_go(df, target_vr), axis=1)

    # Menambahkan kolom untuk target VR
    df['Target VR'] = target_vr

    # Menampilkan data kapal dengan VR dan rate to go
    st.write("Data Kapal dengan VR dan Rate to Go:")
    st.write(df[['Vessel', 'Month', 'VR', 'Target VR', 'Rate to Go']])

    # Menyimpan kembali ke file Excel menggunakan BytesIO untuk membuat file Excel
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()

    # Menyimpan kembali ke file Excel dan menyediakan tombol unduh
    excel_data = to_excel(df)
    st.download_button("Unduh Data Kapal yang Diperbarui", data=excel_data, file_name='updated_vessel_data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
