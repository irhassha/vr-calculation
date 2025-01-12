import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# 1. Title dan Upload Data
st.title("Forecast Yard Occupancy Ratio (YOR) Harian")
uploaded_file = st.file_uploader("Upload data CSV", type="csv")

if uploaded_file:
    # 2. Load Data
    data = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.dataframe(data.head())

    # 3. Pilih Kolom untuk Model
    target_col = st.selectbox("Pilih kolom target (YOR):", data.columns)
    feature_cols = st.multiselect("Pilih kolom fitur:", data.columns)

    if target_col and feature_cols:
        # 4. Model Regresi
        X = data[feature_cols]
        y = data[target_col]
        model = LinearRegression()
        model.fit(X, y)

        # Prediksi
        predictions = model.predict(X)
        st.write("Koefisien Model:")
        st.write(model.coef_)

        # 5. Plot Hasil
        plt.figure(figsize=(10, 5))
        plt.plot(y, label="Actual")
        plt.plot(predictions, label="Predicted")
        plt.legend()
        st.pyplot(plt)

        # 6. Monte Carlo Simulation
        st.header("Simulasi Monte Carlo")
        simulations = st.number_input("Jumlah Simulasi", min_value=100, max_value=10000, value=1000, step=100)

        if simulations:
            results = []
            for _ in range(simulations):
                # Sampling input (contoh dengan distribusi normal)
                sampled_X = X.apply(lambda col: np.random.normal(col.mean(), col.std()), axis=0)
                simulated_yor = model.predict(sampled_X)
                results.append(simulated_yor.mean())

            # Distribusi hasil simulasi
            st.write("Hasil Simulasi Monte Carlo:")
            plt.hist(results, bins=30, alpha=0.7)
            plt.xlabel("YOR")
            plt.ylabel("Frekuensi")
            st.pyplot(plt)
