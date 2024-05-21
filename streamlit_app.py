import streamlit as st
import random

st.title("生物ガチャアプリ")
st.text("このガチャを通して、生物について学ぼう！")

if st.button("ガチャを回しましょう。"):
    results = ["鰯","蛙","蛇","雀","猿"]
    result = random.choice(results)
    st.text(result + "、特徴言える？")