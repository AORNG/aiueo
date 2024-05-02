import streamlit as st
import random
st.title("おみくじアプリ")
#ユーザー名の入力
user_name=st.text_input("あなたの名前を入力してください。")
if st.button("おみくじを引く"):
    results=["大吉","中吉","小吉","吉","凶","大凶"]
    result=random.choice(results)

#結果に応じたコメントやアドバイス
comments={
    "大吉":"わあー"
    "中吉":"おおー"
    "小吉":"まあまあ"
    "吉":"そうか"
    "凶":"ドンマイ"
    "大凶":"はっはっは"
}

#結果とコメントの表示
if user_name:
    st.write(f"結果:{result}")

    st.write(comments[result]")