import streamlit as st
import plotly.express as px
from utils import load_data

df = load_data()

st.title("📊 장르별 성공 확률 분석")

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

genre_stats = (
    df.groupby("장르")
    .agg(
        전체게임수=("Name", "count"),
        성공게임수=("Success", "sum"),
        평균판매량=("Global_Sales", "mean")
    )
    .reset_index()
)

genre_stats["성공확률"] = genre_stats["성공게임수"] / genre_stats["전체게임수"] * 100
genre_stats = genre_stats.sort_values("성공확률", ascending=False)

st.markdown("### ✅ 장르별 성공 확률")
st.caption("Global_Sales가 1 이상이면 100만 장 이상 판매된 게임으로 보고 성공으로 분류했습니다.")

fig = px.bar(
    genre_stats,
    x="장르",
    y="성공확률",
    text=genre_stats["성공확률"].round(1),
    title="장르별 성공 확률 (%)"
)

fig.update_traces(textposition="outside")
fig.update_layout(
    height=520,
    xaxis_title="게임 장르",
    yaxis_title="성공 확률 (%)",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### 🎮 장르 선택해서 자세히 보기")

selected_genre = st.selectbox(
    "분석할 장르를 선택하세요",
    genre_stats["장르"].tolist()
)

selected = genre_stats[genre_stats["장르"] == selected_genre].iloc[0]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("전체 게임 수", f"{int(selected['전체게임수']):,}개")

with col2:
    st.metric("성공 게임 수", f"{int(selected['성공게임수']):,}개")

with col3:
    st.metric("성공 확률", f"{selected['성공확률']:.1f}%")

st.info(
    f"{selected_genre} 장르는 전체 {int(selected['전체게임수']):,}개 중 "
    f"{int(selected['성공게임수']):,}개가 100만 장 이상 판매되었습니다."
)

st.markdown("### 📋 장르별 분석표")
st.dataframe(genre_stats, use_container_width=True)
