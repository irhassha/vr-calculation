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

# Sidebar
with st.sidebar:
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

# Main content area
if uploaded_file is not None:
    # Read uploaded Excel file
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    
    # Display column names to check existing columns (optional, can be removed)
    # st.write("Column names in the Excel file:", df.columns)
    
    # Check if necessary columns exist
    required_columns = ['Vessel', 'Month', 'Disch', 'Load', 'TS SHF', 'CI', 'GCR', 'MB']
    
    # Check if all required columns exist in the data
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
        
        # Display ship data with calculated VR
        st.write("Ship Data with calculated VR:", df)
        
        # Select option whether VR calculation is based on month or overall
        time_period = st.selectbox("Select VR calculation period", ["Overall", "Per Month"])
        
        if time_period == "Per Month":
            # Calculate average VR per month
            month = st.selectbox("Select month", df['Month'].unique())
            df_filtered = df[df['Month'] == month]
            avg_vr = df_filtered['VR'].mean()
            st.write(f"Average VR for {month}: {round(avg_vr, 2)}")
        else:
            # Overall average VR
            avg_vr = df['VR'].mean()
            st.write(f"Overall average VR: {round(avg_vr, 2)}")

        # Display input for target VR and estimated number of next ships
        col1, col2 = st.columns(2)  # Bagi area menjadi 2 kolom
        with col1:
            target_vr = st.number_input("Enter target VR to be achieved", min_value=0, value=80)
        with col2:
            estimated_ships = st.number_input("Enter estimated number of next ships", min_value=1, value=5)
        
        # Calculate total VR needed to achieve the target average VR
        total_ships = len(df) + estimated_ships
        total_vr_needed = total_ships * target_vr
        
        # Calculate total existing VR
        total_current_vr = len(df) * avg_vr
        
        # Calculate total VR that needs to be added by the next ship
        vr_needed_by_new_ships = total_vr_needed - total_current_vr
        
        # Calculate the average VR required by the next ship
        average_vr_for_new_ships = vr_needed_by_new_ships / estimated_ships
        
        # Display Rate to Go results
        st.write(f"Average VR required by the next ship to reach the target: {round(average_vr_for_new_ships, 2)}")
