import streamlit as st
import pandas as pd

# Fungsi untuk menghitung VR
def calculate_vr(discharge, load, crane_intensity, crane_performance, meal_break):
    vr = (discharge + load) / (((discharge + load) / crane_intensity / crane_performance) + meal_break)
    return vr

# Upload CSV untuk data kapal
st.title('Kalkulator VR Kapal')

# Upload file CSV
uploaded_file = st.file_uploader("Unggah Data Kapal (CSV)", type=["csv"])

# Jika file di-upload, load data dan tampilkan
if uploaded_file is not None:
    # Membaca file CSV
    df = pd.read_csv(uploaded_file)
    st.write("Data Kapal yang Diupload:")
    st.write(df)

    # Memastikan kolom yang dibutuhkan ada
    required_columns = ['Vessel', 'ETA', 'Jumlah Bongkar', 'Jumlah Muat', 'Crane Intensity', 'Performance Crane', 'Meal Break Time']
    for col in required_columns:
        if col not in df.columns:
            st.error(f"Kolom '{col}' tidak ditemukan dalam file CSV.")
            break
else:
    st.info("Silakan unggah file CSV dengan data kapal.")

# Input untuk menambahkan kapal baru
vessel_name = st.text_input('Nama Kapal:')
eta = st.text_input('ETA Kapal:')
discharge_quantity = st.number_input('Jumlah Bongkar (TEU):', min_value=0)
load_quantity = st.number_input('Jumlah Muat (TEU):', min_value=0)
crane_intensity = st.number_input('Crane Intensity (Penggunaan Crane):', min_value=0)
crane_performance = st.number_input('Performance Crane per Jam:', min_value=0)
meal_break_time = st.number_input('Total Waktu Meal Break (Jam):', min_value=0)

# Target average VR
target_vr = st.number_input('Target Average VR:', min_value=0)

# Hitung VR untuk kapal tersebut
if vessel_name:
    vr = calculate_vr(discharge_quantity, load_quantity, crane_intensity, crane_performance, meal_break_time)
    st.write(f"VR untuk kapal {vessel_name} adalah: {vr:.2f}")
    
    # Rate-to-go VR dibandingkan dengan target average VR
    if target_vr > 0:
        rate_to_go = vr / target_vr
        st.write(f"Rate-to-go VR dibandingkan dengan target VR adalah: {rate_to_go:.2f}")
    else:
        st.write("Target Average VR harus lebih besar dari 0.")

# Menambahkan kapal baru ke dalam dataframe yang sudah ada (CSV upload atau data internal)
if uploaded_file is not None:
    new_data = pd.DataFrame([[vessel_name, eta, discharge_quantity, load_quantity, crane_intensity, crane_performance, meal_break_time]], 
                            columns=df.columns)
    df = pd.concat([df, new_data], ignore_index=True)
    st.write("Data Kapal Setelah Penambahan:")
    st.write(df)
    
    # Menyimpan kembali ke file CSV
    csv_data = df.to_csv(index=False)
    st.download_button("Unduh Data Kapal yang Diperbarui", data=csv_data, file_name='updated_vessel_data.csv', mime='text/csv')

# Menampilkan data kapal dan VR yang telah dihitung rata-ratanya
if uploaded_file is not None:
    # Menghitung VR untuk semua kapal di data
    df['VR'] = df.apply(lambda row: calculate_vr(row['Jumlah Bongkar'], row['Jumlah Muat'], row['Crane Intensity'], 
                                                 row['Performance Crane'], row['Meal Break Time']), axis=1)
    
    # Menampilkan data kapal dengan VR
    st.write("Data Kapal dan VR:")
    st.write(df[['Vessel', 'VR']])

    # Menghitung rata-rata VR dari semua kapal
    average_vr = df['VR'].mean()
    st.write(f"Rata-rata VR dari semua kapal: {average_vr:.2f}")
