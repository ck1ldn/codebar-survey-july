import streamlit as st
import pandas as pd

csv_url = 'https://docs.google.com/spreadsheets/d/1E9mHJl7o80goyECXu631EhN3bW8OHPiNVLNr5C5JkyA/export?format=csv'

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data(csv_url)

st.title("Survey Results Dashboard")
st.dataframe(df)
