import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="데이터 보기",
    page_icon="📄",
    layout="wide"
)

st.title("📄 원본 데이터 보기")

df = pd.read_csv("vgsales.csv")

df = df.dropna(subset=["Year", "Genre", "Global_Sales"])
df["Year"] = df["Year"].astype(int)

df["성공여부"] = df["Global_Sales"].apply(lambda x: "성공" if x >= 1 else "실패")

st.write("게임 판매량 데이터 중 분석에 필요한 컬럼을 확인할 수 있습니다.")

columns = ["Name", "Platform", "Year", "Genre", "Publisher", "Global_Sales", "성공여부"]

st.dataframe(df[columns])

st.subheader("장르 선택해서 보기")

genre = st.selectbox("장르를 선택하세요", sorted(df["Genre"].unique()))

filtered = df[df["Genre"] == genre]

st.write(f"선택한 장르: **{genre}**")
st.write(f"게임 수: {len(filtered)}개")

st.dataframe(filtered[columns])
