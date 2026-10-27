
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

DB_PATH = Path(r"C:\nandish\sam projects\AmazonIndiaProject\data\amazon_india_analytics.db")

st.set_page_config(page_title="Amazon India Sales Analytics", layout="wide")
st.title("Amazon India: A Decade of Sales Analytics")
st.caption("Sales performance dashboard | 2015–2025")

@st.cache_data
def load_data():
    with sqlite3.connect(DB_PATH) as conn:
        kpis = pd.read_sql_query("""
            SELECT
                SUM(final_amount_inr) AS revenue,
                COUNT(*) AS transactions,
                SUM(quantity) AS units,
                COUNT(DISTINCT customer_id) AS customers
            FROM transactions
        """, conn)

        yearly = pd.read_sql_query("""
            SELECT order_year AS year,
                   SUM(final_amount_inr) AS revenue,
                   COUNT(*) AS transactions
            FROM transactions
            GROUP BY order_year
            ORDER BY order_year
        """, conn)

        categories = pd.read_sql_query("""
            SELECT category,
                   SUM(final_amount_inr) AS revenue
            FROM transactions
            GROUP BY category
            ORDER BY revenue DESC
        """, conn)

        payments = pd.read_sql_query("""
            SELECT payment_method,
                   SUM(final_amount_inr) AS revenue
            FROM transactions
            GROUP BY payment_method
            ORDER BY revenue DESC
        """, conn)

    return kpis, yearly, categories, payments

kpis, yearly, categories, payments = load_data()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"₹{kpis.loc[0, 'revenue']:,.0f}")
col2.metric("Transactions", f"{kpis.loc[0, 'transactions']:,.0f}")
col3.metric("Units Sold", f"{kpis.loc[0, 'units']:,.0f}")
col4.metric("Unique Customers", f"{kpis.loc[0, 'customers']:,.0f}")

st.subheader("Yearly Revenue Trend")
st.line_chart(yearly.set_index("year")["revenue"])

st.subheader("Yearly Transaction Volume")
st.bar_chart(yearly.set_index("year")["transactions"])

st.subheader("Revenue by Category")
st.bar_chart(categories.set_index("category")["revenue"])

st.subheader("Revenue by Payment Method")
st.bar_chart(payments.set_index("payment_method")["revenue"])

st.subheader("Yearly Revenue Data")
st.dataframe(yearly, use_container_width=True)

st.subheader("Category Performance")
st.dataframe(categories, use_container_width=True)
