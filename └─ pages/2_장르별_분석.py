import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="장르별 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 장르별 성공확률 분석")

df = pd.read_csv("vgsales.csv")

df = df.dropna(subset=["Year", "Genre", "Global_Sales"])
df["Year"] = df["Year"].astype(int)

df["성공여부"] = df["Global_Sales"].apply(lambda x: 1 if x >= 1 else 0)

genre_stats = df.groupby("Genre").agg(
    전체게임수=("Name", "count"),
    성공게임수=("성공여부", "sum"),
    평균판매량=("Global_Sales", "mean")
).reset_index()

genre_stats["성공확률"] = genre_stats["성공게임수"] / genre_stats["전체게임수"] * 100

st.subheader("장르별 성공확률 표")
st.dataframe(genre_stats.sort_values("성공확률", ascending=False))

st.subheader("장르별 성공확률 그래프")

chart_data = genre_stats.sort_values("성공확률", ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(chart_data["Genre"], chart_data["성공확률"])
ax.set_xlabel("Genre")
ax.set_ylabel("Success Rate (%)")
ax.set_title("Success Rate by Genre")
plt.xticks(rotation=45)

st.pyplot(fig)

st.subheader("장르 하나 자세히 보기")

genre = st.selectbox("장르 선택", sorted(df["Genre"].unique()))

selected = genre_stats[genre_stats["Genre"] == genre].iloc[0]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("전체 게임 수", int(selected["전체게임수"]))

with col2:
    st.metric("성공 게임 수", int(selected["성공게임수"]))

with col3:
    st.metric("성공확률", f"{selected['성공확률']:.2f}%")

st.write(f"""
**{genre} 장르**는 전체 {int(selected['전체게임수'])}개 게임 중  
{int(selected['성공게임수'])}개가 100만 장 이상 판매되었습니다.
""")
