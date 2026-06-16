import streamlit as st
from utils import load_data

df = load_data()

st.title("📄 Dataset Explorer")

genre = st.multiselect(
    "장르 선택",
    df["Genre"].unique()
)

if genre:
    df = df[df["Genre"].isin(genre)]

st.dataframe(
    df,
    use_container_width=True,
    height=600
)
