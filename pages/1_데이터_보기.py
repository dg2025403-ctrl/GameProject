import streamlit as st
from utils import load_data

st.set_page_config(
    page_title="데이터 보기",
    page_icon="📄",
    layout="wide"
)

st.title("📄 게임 데이터 보기")

st.markdown("""
### 🎮 게임 데이터 탐색기

원본 게임 판매량 데이터를 확인하고,  
장르별 게임 정보를 쉽게 탐색할 수 있습니다.
""")

df = load_data()

df = df.rename(columns={
    "Name": "게임명",
    "Platform": "게임기",
    "Year": "출시연도",
    "Publisher": "제작사",
    "Global_Sales": "판매량(백만장)"
})

columns = [
    "게임명",
    "게임기",
    "출시연도",
    "장르",
    "제작사",
    "판매량(백만장)",
    "성공여부"
]

st.subheader("🔎 장르별 데이터 검색")

genre = st.selectbox(
    "🎮 게임 장르 선택",
    sorted(df["장르"].unique())
)

filtered = df[df["장르"] == genre]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("선택한 장르", genre)

with col2:
    st.metric("게임 수", f"{len(filtered):,}개")

with col3:
    st.metric("평균 판매량", f"{filtered['판매량(백만장)'].mean():.2f}M")

st.dataframe(
    filtered[columns],
    use_container_width=True,
    height=500
)

st.subheader("📋 전체 데이터 미리보기")

st.dataframe(
    df[columns],
    use_container_width=True,
    height=500
)
