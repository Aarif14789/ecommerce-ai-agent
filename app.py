import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from llm_sql import question_to_sql_groq

# -------------------- Page Configuration --------------------
st.set_page_config(page_title="E-commerce AI Assistant", layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #f4f6f7;
    font-family: 'Segoe UI', sans-serif;
}
.title-banner {
    background-color: #2c3e50;
    color: white;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 1.5rem;
}
.title-banner h1 {
    font-size: 2.2rem;
    margin: 0;
}
.footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    text-align: center;
    color: gray;
    font-size: 0.75rem;
    padding: 0.5rem;
}
.confidential-tag {
    background-color: #e74c3c;
    color: white;
    padding: 0.3rem 0.7rem;
    border-radius: 5px;
    font-size: 0.8rem;
    display: inline-block;
    margin-bottom: 10px;
}
</style>

<div class="title-banner">
    <h1>🛍️ E-commerce AI Assistant</h1>
    <div class="confidential-tag">Confidential — For Internal Use Only</div>
</div>
""", unsafe_allow_html=True)

# -------------------- Input Section --------------------
question = st.text_input("💬 Ask your question:", placeholder="e.g., Which product has the highest RoAS?")

if question:
    with st.spinner("🔍 Generating SQL and fetching results..."):
        sql_query = question_to_sql_groq(question)
        st.code(sql_query, language="sql")

        try:
            conn = sqlite3.connect("ecommerce.db")
            df = pd.read_sql_query(sql_query, conn)
            conn.close()
        except Exception as e:
            st.error(f"❌ SQL Error: {e}")
            st.stop()

    if df.empty:
        st.warning("⚠️ No results found.")
        st.stop()

    st.success("✅ Query executed successfully!")

    tab1, tab2 = st.tabs(["📊 Visualization", "📋 Data Table"])

    # -------- Visualization Blocks --------
    if "total_sales" in df.columns:
        with tab1:
            chart_type = st.radio("📈 Chart type:", ["Bar Chart", "Pie Chart"], horizontal=True)
            if chart_type == "Bar Chart":
                fig = px.bar(df, x="item_id", y="total_sales", color="total_sales",
                             title="Total Sales by Product", color_continuous_scale="Blues")
            else:
                fig = px.pie(df, names="item_id", values="total_sales",
                             title="Sales Distribution", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.dataframe(df)

    elif "roas" in df.columns:
        with tab1:
            if "item_id" in df.columns and len(df) > 1:
                top_n = st.slider("🏆 Top N Products by RoAS", 1, len(df), min(10, len(df)))
                df_top = df.sort_values("roas", ascending=False).head(top_n)
                fig = px.bar(df_top, x="item_id", y="roas", color="roas",
                             title="Top Products by RoAS", text_auto=".2f",
                             color_continuous_scale="Teal")
                st.plotly_chart(fig, use_container_width=True)
                with tab2:
                    st.dataframe(df_top)
            else:
                st.metric("📈 RoAS", f"{df['roas'].iloc[0]:.2f}")
                with tab2:
                    st.dataframe(df)

    elif "CPC" in df.columns:
        with tab1:
            df_sorted = df.sort_values("CPC", ascending=False)
            fig = px.bar(df_sorted, x="item_id", y="CPC", color="CPC",
                         title="Cost Per Click (CPC) by Product", color_continuous_scale="Magma")
            st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns(2)
            col1.metric("🔺 Highest CPC", f"${df_sorted.iloc[0]['CPC']:.2f}")
            col2.metric("🔻 Lowest CPC", f"${df_sorted.iloc[-1]['CPC']:.2f}")

        with tab2:
            st.dataframe(df_sorted)

    else:
        st.info("ℹ️ No specific visualization template found.")
        st.dataframe(df)

# -------------------- Footer (Confidential + Author) --------------------
st.markdown("""
<div class="footer">
    Developed by <strong>Arif (21MID0043)</strong> — E-commerce AI Assistant Project | All rights reserved © 2025
</div>
""", unsafe_allow_html=True)
