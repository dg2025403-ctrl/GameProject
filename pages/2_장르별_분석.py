import streamlit as st
import plotly.express as px
from utils import load_data

df = load_data()

st.title("📊 Genre Analysis")

genre_stats = (
    df.groupby("Genre")
      .agg(
        Games=("Name","count"),
        Success=("Success","sum")
      )
)

genre_stats["SuccessRate"] = (
    genre_stats["Success"]
    /
    genre_stats["Games"]
    *100
)

fig = px.bar(
    genre_stats,
    y="SuccessRate",
    title="장르별 성공확률"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
