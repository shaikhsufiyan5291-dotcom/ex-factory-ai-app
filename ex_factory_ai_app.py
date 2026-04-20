import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# --------------------------------------------------
# Page setup
# --------------------------------------------------
st.set_page_config(
    page_title="Ex‑Factory AI Analyst",
    layout="wide"
)

st.title("🧠 Ex‑Factory AI Analyst")
st.caption("Upload → Answer → Analyze | Ex‑Factory Performance Intelligence")

# --------------------------------------------------
# Upload Excel
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "📤 Upload Ex‑Factory Excel File",
    type=["xlsx"]
)

if uploaded_file:

    # Read file
    df = pd.read_excel(uploaded_file)
    st.success("✅ File uploaded successfully")

    st.subheader("🔍 AI detected these columns")
    st.write(list(df.columns))

    # --------------------------------------------------
    # AI‑style configuration (in sidebar)
    # --------------------------------------------------
    with st.sidebar:
        st.header("🧠 AI Configuration")

        date_col = st.selectbox("📅 Date column", df.columns)
        invoice_col = st.selectbox("🧾 Invoice column", df.columns)
        customer_col = st.selectbox("👤 Customer column", df.columns)
        qty_col = st.selectbox("📦 Quantity column", df.columns)

        base_col = st.selectbox("💰 Ex‑Factory (Basic) value column", df.columns)
        gst_col = st.selectbox("🧾 GST / Tax column", df.columns)
        transport_col = st.selectbox("🚚 Transport cost column", df.columns)
        loading_col = st.selectbox("🏗️ Loading cost column", df.columns)

        focus = st.radio(
            "🎯 Performance focus",
            ["Invoice", "Customer"]
        )

        target_margin = st.slider(
            "🎯 Target Margin %",
            min_value=0,
            max_value=50,
            value=18
        )

        raw_cost_per_unit = st.number_input(
            "🧱 Raw material cost per unit",
            value=0.0
        )

    # --------------------------------------------------
    # Calculations
    # --------------------------------------------------
    df_calc = df.copy()

    df_calc["NET_SALES"] = (
        df_calc[base_col]
        - df_calc[transport_col]
        - df_calc[loading_col]
    )

    df_calc["RAW_COST"] = df_calc[qty_col] * raw_cost_per_unit
