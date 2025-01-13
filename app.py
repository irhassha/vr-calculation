import streamlit as st
import pandas as pd

st.markdown(
    """
    <style>
    body {
        background-color: #F0F8FF;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add title
st.title("VR Calculation")

# Function to calculate VR
def calculate_vr(discharge, load, TS_SHF, CI, GCR, MB):
    try:
        vr = (discharge + load + TS_SHF) / (((discharge + load + TS_SHF) / CI / GCR) + MB)
        return round(vr,2)
    except ZeroDivisionError:
        return 0

# Sidebar
with st.sidebar:
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

# Main content area
if uploaded_file is not None:
    # Read uploaded Excel file
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    
    # ... (kode untuk memeriksa kolom)

    # Calculate VR for each ship
    df['VR'] = df.apply(lambda row: calculate_vr(
        row['Disch'], row['Load'], row['TS SHF'], row['CI'],
        row['GCR'], row['MB']), axis=1)
    
    # ... (kode untuk menampilkan tabel dan elemen lainnya)
