import streamlit as st
import pandas as pd

# Contoh DataFrame
data = {
    "Vessel": ["A", "B", "C"],
    "Month": ["Jan", "Feb", "Mar"],
    "VR": [80, 75, 85],
}
df = pd.DataFrame(data)

st.write("Data Editor Test")
edited_df = st.experimental_data_editor(df, num_rows="dynamic")
st.write("Hasil:")
st.write(edited_df)
