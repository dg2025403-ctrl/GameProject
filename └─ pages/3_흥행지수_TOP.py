import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="흥행지수 TOP",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 장르별 흥행지수 TOP")

df = pd.read_csv("vgsales.csv")

df = df.dropna(subset=["Year", "Genre", "Global_Sales"])
df["Year"] = df["Year"].astype(int)

df["성공여부"] = df["Global_Sales"].apply(lambda x: 1 if x >= 1 else 0)

latest_year = df["Year"].max()
recent_df = df[df["Year"] >= latest_year - 5]

genre_stats = df.groupby("Genre").agg(
    전체게임수=("Name", "count"),
    성공게임수=("성공여부", "sum"),
    전체평균판매량=("Global_Sales", "mean")
).reset_index()

recent_stats = recent_df.groupby("Genre").agg(
    최근평균판매량=("Global_Sales", "mean")
).reset_index()

result = pd.merge(genre_stats, recent_stats, on="Genre", how="left")

result["성공확률"] = result["성공게임수"] / result["전체게임수"] * 100
result["성장성"] = result["최근평균판매량"] / result["전체평균판매량"]
result["성장성"] = result["성장성"].fillna(0)

result["흥행지수"] = result["성공확률"] * 0.6 + result["성장성"] * 40

result = result.sort_values("흥행지수", ascending=False)

st.subheader("새롭게 만든 데이터: 흥행지수")

st.code("""
흥행지수 = 성공확률 * 0.6 + 성장성 * 40
""")

st.dataframe(result)

st.subheader("흥행지수 TOP 5")

top5 = result.head(5)

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(top5["Genre"], top5["흥행지수"])
ax.set_xlabel("Genre")
ax.set_ylabel("흥행지수")
ax.set_title("Top 5 Genre by Success Index")

st.pyplot(fig)

st.subheader("1위 장르 분석")

top_genre = result.iloc[0]

st.success(f"""
흥행지수가 가장 높은 장르는 **{top_genre['Genre']}**입니다.

성공확률: {top_genre['성공확률']:.2f}%  
성장성: {top_genre['성장성']:.2f}  
흥행지수: {top_genre['흥행지수']:.2f}
""")

st.subheader("게임별 판매량 TOP 10")

top_games = df.sort_values("Global_Sales", ascending=False).head(10)

st.dataframe(top_games[["Name", "Platform", "Year", "Genre", "Global_Sales"]])
