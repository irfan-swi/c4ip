import streamlit as st
import duckdb
import pandas as pd

# Title for the app
st.title("Patent Data Explorer")

@st.cache(allow_output_mutation=True)
def get_connection():
    return duckdb.connect(database='uspto.duckdb', read_only=True)

conn = get_connection()

# Fetching table names
query = "SELECT table_name FROM information_schema.tables WHERE table_schema='main';"
tables = pd.read_sql(query, conn)

# Layout adjustments using columns
col1, col2 = st.columns([1, 3])

with col1:
    table_name = st.selectbox('Select a table', tables['table_name'])

if table_name:
    query_columns = f"PRAGMA table_info({table_name})"
    columns = pd.read_sql(query_columns, conn)
    
    with col2:
        selected_columns = st.multiselect('Select columns', columns['name'])

# Button to show data
if st.button('Show 10 sample rows'):
    if table_name and selected_columns:
        query_data = f"SELECT {', '.join(selected_columns)} FROM {table_name} ORDER BY RANDOM() LIMIT 10"
        data = pd.read_sql(query_data, conn)
        st.table(data)
