import streamlit as st
import plotly.express as px
from utils import load_data

df = load_data()

st.title("🏆 장르별 흥행지수 TOP")

genre_kor = {
    "Action": "액션",
    "Adventure": "어드벤처",
    "Fighting": "격투",
    "Misc": "기타",
    "Platform": "플랫폼",
    "Puzzle": "퍼즐",
    "Racing": "레이싱",
    "Role-Playing": "롤플레잉/RPG",
    "Shooter": "슈팅/FPS",
    "Simulation": "시뮬레이션",
    "Sports": "스포츠",
    "Strategy": "전략"
}

df["장르"] = df["Genre"].map(genre_kor).fillna(df["Genre"])

latest_year = df["Year"].max()
recent = df[df["Year"] >= latest_year - 5]

genre = (
    df.groupby("장르")
    .agg(
        전체게임수=("Name", "count"),
        성공게임수=("Success", "sum"),
        전체평균판매량=("Global_Sales", "mean")
    )
)

recent_avg = recent.groupby("장르")["Global_Sales"].mean()

genre["최근평균판매량"] = recent_avg
genre["최근평균판매량"] = genre["최근평균판매량"].fillna(0)

genre["성공확률"] = genre["성공게임수"] / genre["전체게임수"] * 100
genre["성장성"] = genre["최근평균판매량"] / genre["전체평균판매량"]
genre["성장성"] = genre["성장성"].fillna(0)

genre["흥행지수"] = genre["성공확률"] * 0.6 + genre["성장성"] * 40
genre = genre.sort_values("흥행지수", ascending=False).reset_index()

st.markdown("### 🧮 흥행지수 계산식")

st.code("""
흥행지수 = 성공확률 × 0.6 + 성장성 × 40

성공확률 = 100만 장 이상 판매된 게임 비율
성장성 = 최근 5년 평균 판매량 / 전체 평균 판매량
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("1위 장르", genre.iloc[0]["장르"])

with col2:
    st.metric("최고 흥행지수", f"{genre.iloc[0]['흥행지수']:.1f}점")

with col3:
    st.metric("분석 장르 수", f"{len(genre)}개")

st.markdown("### 🏆 흥행지수 TOP 10")

fig = px.bar(
    genre.head(10),
    x="장르",
    y="흥행지수",
    text=genre.head(10)["흥행지수"].round(1),
    title="장르별 흥행지수 TOP 10"
)

fig.update_traces(textposition="outside")
fig.update_layout(
    height=520,
    xaxis_title="게임 장르",
    yaxis_title="흥행지수",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### 📋 흥행지수 전체표")

show = genre.copy()
show["성공확률"] = show["성공확률"].round(2)
show["성장성"] = show["성장성"].round(2)
show["흥행지수"] = show["흥행지수"].round(2)
show["전체평균판매량"] = show["전체평균판매량"].round(2)
show["최근평균판매량"] = show["최근평균판매량"].round(2)

st.dataframe(show, use_container_width=True)
