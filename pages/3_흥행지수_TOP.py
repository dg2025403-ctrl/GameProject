import streamlit as st
import plotly.express as px
from utils import load_data

df = load_data()

st.title("🏆 Success Index Ranking")

latest = df["Year"].max()

recent = df[
    df["Year"] >= latest-5
]

genre = (
    df.groupby("Genre")
      .agg(
        Games=("Name","count"),
        Success=("Success","sum"),
        AvgSales=("Global_Sales","mean")
      )
)

recent_avg = (
    recent.groupby("Genre")
    ["Global_Sales"]
    .mean()
)

genre["Growth"] = (
    recent_avg
    /
    genre["AvgSales"]
)

genre["SuccessRate"] = (
    genre["Success"]
    /
    genre["Games"]
    *100
)

genre["Index"] = (
    genre["SuccessRate"]*0.6
    +
    genre["Growth"]*40
)

genre = genre.sort_values(
    "Index",
    ascending=False
)

st.dataframe(
    genre,
    use_container_width=True
)

fig = px.bar(
    genre.head(10),
    y="Index",
    title="흥행지수 TOP 장르"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

winner = genre.index[0]

st.success(
    f"🥇 가장 유망한 장르 : {winner}"
)
