import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

if uploaded_file:

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

    k1, k2, k3 = st.columns(3)
    k1.metric("Total Ex‑Factory Sales", round(df_calc[base_col].sum(), 2))
    k2.metric("Total Margin", round(df_calc["MARGIN"].sum(), 2))
    k3.metric(
        "Records Below Target Margin",
        len(df_calc[df_calc["MARGIN_%"] < target_margin])
    )

    # Alert: loss‑making records
    loss_df = df_calc[df_calc["MARGIN"] < 0]
    if not loss_df.empty:
        st.error(f"❌ {len(loss_df)} records are loss‑making")

    # --------------------------------------------------
    # Focus view
    # --------------------------------------------------
    st.subheader(f"🎯 Focus: {focus} Level Performance")

    if focus == "Invoice":
        view = df_calc.groupby(invoice_col).agg(
            Sales=(base_col, "sum"),
            Margin=("MARGIN", "sum"),
            Margin_Percent=("MARGIN_%", "mean")
        ).reset_index()
        x_col = invoice_col
    else:
        view = df_calc.groupby(customer_col).agg(
            Sales=(base_col, "sum"),
            Margin=("MARGIN", "sum"),
            Margin_Percent=("MARGIN_%", "mean")
        ).reset_index()
        x_col = customer_col

    st.dataframe(view, use_container_width=True)

    # --------------------------------------------------
    # Visualization (NO seaborn)
    # --------------------------------------------------
    st.subheader("📈 Top 10 Margin Contributors")

    top10 = view.sort_values("Margin", ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.bar(top10[x_col].astype(str), top10["Margin"])
    ax.set_ylabel("Margin")
    ax.set_title("Top 10 Margin Contributors")
    plt.xticks(rotation=45)

    st.pyplot(fig)

else:
m
