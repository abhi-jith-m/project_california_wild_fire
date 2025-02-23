import streamlit as st
import pandas as pd
from Data import Data
if 'key' not in st.session_state:
    st.session_state.page="home"

st.set_page_config(layout="wide")

path = r"Dataset\california.csv"
df=pd.read_csv(path,low_memory=False)
Data(df)



