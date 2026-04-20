import streamlit as st
import pandas as pd
import numpy as np

# --------------------------------------------------
# Page configuration
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

if uploaded_file is not None:
    # Read Excel
    df = pd.read_excel(uploaded_file)
    st.success("✅ File uploaded successfully")

    st.subheader("🔍 AI detected these columns")
    st.write(list(df.columns))

    # --------------------------------------------------
    # AI‑style configuration (Sidebar)
    # --------------------------------------------------
    with st.sidebar:
        st.header("🧠 AI Configuration")

        date_col = st.selectbox("📅 Date column", df.columns)
        invoice_col = st.selectbox("🧾 Invoice column", df.columns)
        customer_col = st.selectbox("👤 Customer column", df.columns)
        qty_col = st.selectbox("📦 Quantity column", df.columns)

        base_col = st.selectbox("💰 Ex‑Factory (Basic) value column", df.columns)
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
    df_calc["MARGIN"] = df_calc["NET_SALES"] - df_calc["RAW_COST"]

    df_calc["MARGIN_%"] = np.where(
        df_calc["NET_SALES"] != 0,
        (df_calc["MARGIN"] / df_calc["NET_SALES"]) * 100,
        0
    )

    # --------------------------------------------------
    # KPIs
    # --------------------------------------------------
    st.subheader("📊 Ex‑Factory Performance Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Ex‑Factory Sales", round(df_calc[base_col].sum(), 2))
    col2.metric("Total Margin", round(df_calc["MARGIN"].sum(), 2))
    col3.metric(
        "Below Target % Records",
        len(df_calc[df_calc["MARGIN_%"] < target_margin])
    )

    # Alert: loss‑making records
    loss_df = df_calc[df_calc["MARGIN"] < 0]
    if not loss_df.empty:
        st.error(f"❌ {len(loss_df)} records are loss‑making")

    # --------------------------------------------------
    # Focus View (Table‑based, stable)
    # --------------------------------------------------
    st.subheader(f"🎯 Focus: {focus} Level Performance")

    if focus == "Invoice":
        view = df_calc.groupby(invoice_col).agg(
            Sales=(base_col, "sum"),
            Margin=("MARGIN", "sum"),
            Margin_Percent=("MARGIN_%", "mean")
        ).reset_index()
    else:
        view = df_calc.groupby(customer_col).agg(
            Sales=(base_col, "sum"),
            Margin=("MARGIN", "sum"),
            Margin_Percent=("MARGIN_%", "mean")
        ).reset_index()

    st.dataframe(
        view.sort_values("Margin", ascending=False),
        use_container_width=True
    )

else:
    st.info("⬆️ Upload an Ex‑Factory Excel file to begin analysis")
