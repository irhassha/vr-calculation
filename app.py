import streamlit as st
import pandas as pd

# Fungsi untuk menghitung VR
def calculate_vr(discharge, load, crane_intensity, crane_performance, meal_break):
    vr = (discharge + load) / (((discharge + load) / crane_intensity / crane_performance) + meal_break)
    return vr

# Input data
st.title('Kalkulator VR Kapal')
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
vr = calculate_vr(discharge_quantity, load_quantity, crane_intensity, crane_performance, meal_break_time)

# Menampilkan hasil perhitungan VR
st.write(f"VR untuk kapal {vessel_name} adalah: {vr:.2f}")

# Rate-to-go VR dibandingkan dengan target average VR
if target_vr > 0:
    rate_to_go = vr / target_vr
    st.write(f"Rate-to-go VR dibandingkan dengan target VR adalah: {rate_to_go:.2f}")
else:
    st.write("Target Average VR harus lebih besar dari 0.")

# Menambahkan data kapal ke dalam dataframe (bisa digunakan untuk menghitung rata-rata VR)
if 'vessel_data' not in st.session_state:
    st.session_state.vessel_data = pd.DataFrame(columns=["Vessel", "VR"])

# Menambahkan VR kapal ke dalam data
if st.button('Tambahkan Kapal'):
    new_data = pd.DataFrame([[vessel_name, vr]], columns=["Vessel", "VR"])
    st.session_state.vessel_data = pd.concat([st.session_state.vessel_data, new_data], ignore_index=True)

# Menampilkan data semua kapal yang sudah dihitung VR-nya
st.write("Data Kapal dan VR:")
st.write(st.session_state.vessel_data)

# Menghitung rata-rata VR semua kapal
average_vr = st.session_state.vessel_data['VR'].mean()
st.write(f"Rata-rata VR dari semua kapal: {average_vr:.2f}")

