import pandas as pd
import streamlit as st

import missingno as msno
import plotly.figure_factory as ff

def Data(df):
    path=r"Dataset\Cleaned_cal_dataset.csv"
    df_cleaned=pd.read_csv(path,low_memory=False)
    df.columns = df.columns.str.lstrip('_*#').str.strip()

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Home", "Data", "Charts", "Model"])

    # Home Tab
    with tab1:
        st.write("Welcome to the Home Page!")

    # Data Tab (Sidebar should appear here only)
    with tab2:
        # Display Sidebar only in the Data Tab
        with st.sidebar:
            st.title("Data Sidebar")

            with st.expander("Dataset", expanded=False):
                button_html = """
                    <style>
                    div.stButton > button {
                        background-color: #FF1E1E;
                        color: white;
                        border-radius: 10px;
                        font-size: 16px;
                        font-weight: bold;
                        padding: 10px 20px;
                        border: none;
                        transition: 0.3s;
                        width: 255px;
                    }
                    div.stButton > button:hover {
                        background-color: #FF1E1E;
                        color: white;
                    }
                    div.stButton > button:active {
                        background-color: #FF1E1E;
                        color: black !important;
                    }
                    </style>
                """
                st.markdown(button_html, unsafe_allow_html=True)

                show_table = st.button("Table", key="table_button") 
                show_info = st.button("Info", key="info_button")
                show_desc = st.button("Description", key="desc_button")

            with st.expander("Filters", expanded=False):
                st.title("Filter by column names")
                filters = st.multiselect("Select Columns", df.columns, default=df.columns[:5])
                selectedcols = st.button("Apply", key="sel_button")

                st.title("Filter by values")
                filter_col = st.multiselect("Select Columns", df.columns)
                fil_ter = {}

                if filter_col:
                    for col in filter_col:
                        unique_values = df[col].dropna().astype(str).unique()
                        fil_ter[col] = st.multiselect(f"Select values for {col}", unique_values)

                filter_btn = st.button("Apply", key="fil_button")

           

        # Display Data Tab Content
        if show_table:
            st.dataframe(df, use_container_width=True)
        elif show_info:
            df_info = pd.DataFrame({
                'Columns': df.columns.tolist(),
                "Null count": df.isna().sum().values,
                "Dtype": df.dtypes.values,
            })
            st.dataframe(df_info, use_container_width=True)
        elif show_desc:
            st.dataframe(df.describe(), use_container_width=True)
        elif selectedcols:
            st.dataframe(df[filters], use_container_width=True)
        elif filter_btn:
            if filter_col and any(fil_ter.values()):
                df_filtered = df.copy()
                for col, values in fil_ter.items():
                    if values:  
                        df_filtered = df_filtered[df_filtered[col].astype(str).isin(values)]
                st.dataframe(df_filtered, use_container_width=True)
            else:
                st.warning("Please select at least one column and value to filter!")
        else:
            st.dataframe(df, use_container_width=True)
        
        with st.expander("Missing values"):
            st.write('sooon')
            
        col1, col2 = st.columns(2)
        missing_cols = df.columns[df.isna().mean() * 100 > 50]
        with col1:
            
            df_missing = df[missing_cols]  
            df_missing_summary = df_missing.isna().sum().reset_index()
            df_missing_summary.columns = ['Columns', 'Missing Count']
            st.dataframe(df_missing_summary.sort_values(by='Missing Count',ascending=False).reset_index(drop=True),use_container_width=True)
        with col2:
            df_missing_percent=df_missing.isna().mean()*100
            df_missing_percent=df_missing_percent.reset_index()
            df_missing_percent.columns= ['Columns', 'Missing percent']
            st.dataframe(df_missing_percent.sort_values(by='Missing percent',ascending=False).reset_index(drop=True),use_container_width=True)

        with st.expander("Handling Missing values"):
            st.write('n')
            
        st.markdown("""
        <style>
        .custom-title {
            font-size: 36px !important;
            font-family: 'Fira Code';
            font-weight: bold;
            color: Crimson;
            padding: 10px;
            border-radius: 10px;
        }
        </style>
        <p class="custom-title">Cleaned Dataset</p>
        """, unsafe_allow_html=True)
 
        st.dataframe(df_cleaned.drop('Unnamed: 0',axis=1),use_container_width=True)
        


    # Charts Tab
    with tab3:
        st.write("Charts Section")

    # Model Tab
    with tab4:
        st.write("Model Section")
                