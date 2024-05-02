import streamlit as st
import random
st.title("おみくじアプリ")
if st.button("おみくじを引く"):
    results=["大吉","中吉","小吉","吉","凶","大凶"]
    result=random.choice(results)
    st.wtrite(f"結果:{reuslt}")

