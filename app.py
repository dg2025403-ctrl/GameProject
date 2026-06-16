import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="게임 흥행 분석 사이트",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 게임 판매량 기반 흥행 가능성 분석 사이트")

st.write("""
이 사이트는 게임 판매량 데이터를 활용하여 장르별 성공확률, 성장성, 흥행지수를 분석합니다.

사용 데이터: Video Game Sales Dataset  
새롭게 만든 데이터: 성공 여부, 성공확률, 성장성, 흥행지수
""")

df = pd.read_csv("vgsales.csv")

df = df.dropna(subset=["Year", "Genre", "Global_Sales"])
df["Year"] = df["Year"].astype(int)

df["성공여부"] = df["Global_Sales"].apply(lambda x: "성공" if x >= 1 else "실패")

st.subheader("데이터 기본 정보")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("전체 게임 수", len(df))

with col2:
    st.metric("장르 수", df["Genre"].nunique())

with col3:
    st.metric("평균 판매량", f"{df['Global_Sales'].mean():.2f}M")

st.subheader("사용한 계산식")

st.code("""
성공 여부 = Global_Sales >= 1 이면 성공

성공확률 = 성공한 게임 수 / 전체 게임 수 * 100

성장성 = 최근 5년 평균 판매량 / 전체 평균 판매량

흥행지수 = 성공확률 * 0.6 + 성장성 * 40
""")

st.info("왼쪽 메뉴에서 데이터 보기, 장르별 분석, 흥행지수 TOP 페이지를 선택하세요.")
