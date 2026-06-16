import streamlit as st

st.set_page_config(
    page_title="Game Success Analysis",
    page_icon="🎮",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color:#0e1117;
}

.metric-card {
    background:#262730;
    padding:20px;
    border-radius:15px;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

st.title("🎮 Game Success Analysis")

st.markdown("""
### 게임 판매량 데이터를 이용한 장르별 흥행 가능성 분석

분석 내용

- 성공확률 분석
- 장르별 성장성
- 흥행지수 계산
- TOP 장르 분석
""")

col1,col2,col3 = st.columns(3)

with col1:
    st.info("📊 16,500+ Games")

with col2:
    st.success("🎮 12 Genres")

with col3:
    st.warning("🚀 AI Generated Index")

st.image(
    "https://images.unsplash.com/photo-1511512578047-dfb367046420",
    use_container_width=True
)
