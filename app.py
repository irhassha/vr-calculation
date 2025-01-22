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
st.title("VR and GCR Calculation")

# Function to calculate VR
def calculate_vr(discharge, load, TS_SHF, CI, GCR, MB):
    try:
        vr = (discharge + load + TS_SHF) / (((discharge + load + TS_SHF) / CI / GCR) + MB)
        return round(vr, 2)
    except ZeroDivisionError:
        return 0

# Function to calculate GCR Rate to Go
def calculate_gcr_rate_to_go(current_ships, avg_current_gcr, target_gcr, next_ships):
    try:
        total_ships = current_ships + next_ships
        total_gcr_needed = total_ships * target_gcr
        total_gcr_current = current_ships * avg_current_gcr
        gcr_needed = total_gcr_needed - total_gcr_current
        avg_gcr_for_next_ships = gcr_needed / next_ships
        return avg_gcr_for_next_ships
    except ZeroDivisionError:
        return "Next ships cannot be zero."

# Sidebar
with st.sidebar:
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

# Main content area
if uploaded_file is not None:
    # Read uploaded Excel file
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    
    # Check if necessary columns exist
    required_columns = ['Vessel', 'Month', 'Disch', 'Load', 'TS SHF', 'CI', 'GCR', 'MB']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"The following columns were not found in the data: {', '.join(missing_columns)}")
    else:
        # Calculate VR for each ship
        df['VR'] = df.apply(lambda row: calculate_vr(
            row['Disch'], row['Load'], row['TS SHF'], row['CI'],
            row['GCR'], row['MB']), axis=1)
        
        # Set 'Vessel' column as dataframe index
        df = df.set_index('Vessel')

        # Select option whether VR calculation is based on month or overall
        time_period = st.selectbox("Select VR calculation period", ["Overall", "Per Month"])
        
        if time_period == "Per Month":
            # Calculate average VR per month
            month = st.selectbox("Select month", df['Month'].unique())
            df_filtered = df[df['Month'] == month]
            avg_vr = df_filtered['VR'].mean()
            avg_gcr = df_filtered['GCR'].mean()
            st.write(f"Average VR for {month}: {round(avg_vr, 2)}")
            st.write(f"Average GCR for {month}: {round(avg_gcr, 2)}")
        else:
            # Overall average VR and GCR
            avg_vr = df['VR'].mean()
            avg_gcr = df['GCR'].mean()
            st.write(f"Overall average VR: {round(avg_vr, 2)}")
            st.write(f"Overall average GCR: {round(avg_gcr, 2)}")

        # Display input for target VR, target GCR, and estimated number of next ships
        col1, col2, col3 = st.columns(3)
        with col1:
            target_vr = st.number_input("Enter target VR to be achieved", min_value=0, value=80)
        with col2:
            target_gcr = st.number_input("Enter target GCR to be achieved", min_value=0, value=25)
        with col3:
            estimated_ships = st.number_input("Enter estimated number of next ships", min_value=1, value=5)
        
        # VR calculations
        total_ships = len(df) + estimated_ships
        total_vr_needed = total_ships * target_vr
        total_current_vr = len(df) * avg_vr
        vr_needed_by_new_ships = total_vr_needed - total_current_vr
        average_vr_for_new_ships = vr_needed_by_new_ships / estimated_ships
        
        # GCR calculations
        total_gcr_needed = total_ships * target_gcr
        total_current_gcr = len(df) * avg_gcr
        gcr_needed_by_new_ships = total_gcr_needed - total_current_gcr
        average_gcr_for_new_ships = gcr_needed_by_new_ships / estimated_ships
        
        # Display Rate to Go results
        st.write(f"Average VR Rate to Go: {round(average_vr_for_new_ships, 2)}")
        st.write(f"Average GCR Rate to Go: {round(average_gcr_for_new_ships, 2)}")

        # Display ship data with calculated VR
        st.write("Vessel Data with calculated VR:", df)
