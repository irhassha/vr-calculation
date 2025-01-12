import streamlit as st
import pandas as pd

# Fungsi untuk menghitung VR dengan pengecekan pembagian nol
def calculate_vr(discharge, load, crane_intensity, crane_performance, meal_break):
    if crane_intensity == 0 or crane_performance == 0 or (discharge + load) == 0:
        return 0  # Atau bisa mengembalikan nilai lainnya jika ingin menghindari pembagian dengan nol
    vr = (discharge + load) / (((discharge + load) / crane_intensity / crane_performance) + meal_break)
    return vr

# Upload file Excel untuk data kapal
st.title('Kalkulator VR Kapal')

# Upload file Excel
uploaded_file = st.file_uploader("Unggah Data Kapal (Excel)", type=["xlsx"])

# Jika file di-upload, load data dan tampilkan
if uploaded_file is not None:
    # Membaca file Excel
    df = pd.read_excel(uploaded_file)
    st.write("Data Kapal yang Diupload:")
    st.write(df)

    # Memastikan kolom yang dibutuhkan ada
    required_columns = ['Vessel', 'ETA', 'Jumlah Bongkar', 'Jumlah Muat', 'Crane Intensity', 'Performance Crane', 'Meal Break Time']
    for col in required_columns:
        if col not in df.columns:
            st.error(f"Kolom '{col}' tidak ditemukan dalam file Excel.")
            break
else:
    st.info("Silakan unggah file Excel dengan data kapal.")

# Menambahkan baris baru jika ada tombol tambah
if st.button("Tambah Data Kapal"):
    new_row = {
        'Vessel': '',
        'ETA': '',
        'Jumlah Bongkar': 0,
        'Jumlah Muat': 0,
        'Crane Intensity': 0,
        'Performance Crane': 0,
        'Meal Break Time': 0
    }
    # Menambahkan baris baru ke DataFrame menggunakan pd.concat
    new_df = pd.DataFrame([new_row])
    df = pd.concat([df, new_df], ignore_index=True)

# Menampilkan tabel yang bisa diedit
st.write("Tabel Data Kapal:")
st.write(df)

# Menghitung VR untuk kapal yang ada
df['VR'] = df.apply(lambda row: calculate_vr(row['Jumlah Bongkar'], row['Jumlah Muat'], row['Crane Intensity'], 
                                             row['Performance Crane'], row['Meal Break Time']), axis=1)

# Menampilkan data kapal dengan VR
st.write("Data Kapal dan VR:")
st.write(df[['Vessel', 'VR']])

# Menghitung rata-rata VR dari semua kapal
average_vr = df['VR'].mean()
st.write(f"Rata-rata VR dari semua kapal: {average_vr:.2f}")

# Menyimpan kembali ke file Excel
excel_data = df.to_excel(index=False, engine='openpyxl')
st.download_button("Unduh Data Kapal yang Diperbarui", data=excel_data, file_name='updated_vessel_data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
