import streamlit as st
import duckdb
import pandas as pd

@st.cache_resource
def get_connection():
    return duckdb.connect(database='uspto.duckdb', read_only=True)

conn = get_connection()

query = "SELECT table_name FROM information_schema.tables WHERE table_schema='main';"
tables = pd.read_sql(query, conn)
table_name = st.selectbox('Select a table', tables['table_name'])

if table_name:
    query_columns = f"PRAGMA table_info({table_name})"
    columns = pd.read_sql(query_columns, conn)
    selected_columns = st.multiselect('Select columns', columns['name'])

if st.button('Show first 5 rows'):
    if table_name and selected_columns:
        query_data = f"SELECT {', '.join(selected_columns)} FROM {table_name} LIMIT 5"
        data = pd.read_sql(query_data, conn)
        st.table(data)
