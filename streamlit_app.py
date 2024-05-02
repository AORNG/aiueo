import streamlit as st
import random
st.title("おみくじアプリ")
#ユーザー名の入力
user_name=st.text_input("あなたの名前を入力してください。")
if st.button("おみくじを引く"):
    results=["大吉","中吉","小吉","吉","凶","大凶"]
    result=random.choice(results)
    st.write(f"結果:{result}")

