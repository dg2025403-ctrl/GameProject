import pandas as pd
import streamlit as st

GENRE_KOR = {
    "Action": "액션",
    "Adventure": "어드벤처",
    "Fighting": "격투",
    "Misc": "기타",
    "Platform": "플랫폼 게임",
    "Puzzle": "퍼즐",
    "Racing": "레이싱",
    "Role-Playing": "롤플레잉/RPG",
    "Shooter": "슈팅/FPS",
    "Simulation": "시뮬레이션",
    "Sports": "스포츠",
    "Strategy": "전략"
}

@st.cache_data
def load_data():
    df = pd.read_csv("vgsales.csv")

    df = df.dropna(subset=["Year", "Genre", "Global_Sales"])
    df["Year"] = df["Year"].astype(int)

    df["장르"] = df["Genre"].map(GENRE_KOR).fillna(df["Genre"])
    df["성공여부"] = df["Global_Sales"].apply(lambda x: "성공" if x >= 1 else "실패")
    df["Success"] = (df["Global_Sales"] >= 1).astype(int)

    return df
