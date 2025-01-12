import streamlit as st
import pandas as pd

# Fungsi untuk menghitung VR
def calculate_vr(discharge, load, CI, GCR, MB):
    try:
        vr = (discharge + load) / (((discharge + load) / CI / GCR) + MB)
        return round(vr, 2)
    except ZeroDivisionError:
        return 0

# Inisialisasi df sebagai dataframe kosong
df = pd.DataFrame() 

# Input file excel
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])
if uploaded_file is not None:
    # Membaca file Excel yang di-upload
    df = pd.read_excel(uploaded_file, engine="openpyxl")

    # Mengecek apakah kolom yang diperlukan ada
    required_columns = ['Vessel', 'Month', 'Disch', 'Load', 'CI', 
                        'GCR', 'MB']

    # Mengecek apakah semua kolom yang dibutuhkan ada dalam data
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Kolom-kolom berikut tidak ditemukan dalam data: {', '.join(missing_columns)}")
    else:
        # Menghitung VR untuk setiap kapal JIKA kolom VR belum ada
        if 'VR' not in df.columns:
            df['VR'] = df.apply(lambda row: calculate_vr(
                row['Disch'], row['Load'], row['CI'],
                row['GCR'], row['MB']), axis=1)

        # Mengatur kolom 'Vessel' sebagai index dataframe
        df = df.set_index('Vessel')

        # --- Modifikasi: Form untuk data editor ---
        with st.form("data_editor_form"):  
            edited_df = st.experimental_data_editor(df)
            submit_button = st.form_submit_button("Simpan Perubahan") 

        # --- Modifikasi: JavaScript untuk mengubah label tombol ---
        st.markdown(
            """
            <script>
            const elements = window.parent.document.querySelectorAll('.stMarkdown button');
            for (const element of elements) {
                if (element.textContent === '+') {
                    element.textContent = 'Tambahkan Data';
                }
            }
            </script>
            """,
            unsafe_allow_html=True,
        )

        # Memilih opsi apakah perhitungan VR berdasarkan bulan atau keseluruhan
        time_period = st.selectbox("Pilih periode perhitungan VR", ["Overall", "Per Month"])

        if time_period == "Per Month":
            # Menghitung rata-rata VR per bulan
            month = st.selectbox("Pilih bulan", edited_df['Month'].unique()) # Gunakan edited_df
            df_filtered = edited_df[edited_df['Month'] == month] # Gunakan edited_df
            avg_vr = df_filtered['VR'].mean()
            st.write(f"Rata-rata VR untuk bulan {month}: {round(avg_vr, 2)}") # Perbaikan typo
        else:
            # Rata-rata VR keseluruhan
            avg_vr = edited_df['VR'].mean() # Gunakan edited_df
            st.write(f"Rata-rata VR keseluruhan: {round(avg_vr, 2)}")

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
