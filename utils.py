import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("channels_data_2023-03-19.csv")
    return df