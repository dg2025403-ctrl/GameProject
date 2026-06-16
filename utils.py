import pandas as pd
import streamlit as st

@st.cache_data
def load_data():

    df = pd.read_csv("vgsales.csv")

    df = df.dropna(
        subset=["Year","Genre","Global_Sales"]
    )

    df["Year"] = df["Year"].astype(int)

    df["Success"] = (
        df["Global_Sales"] >= 1
    ).astype(int)

    return df
