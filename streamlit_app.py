import streamlit as st
import pandas as pd
import numpy as np
import random

# Montserratフォントを使ったタイトルを表示
st.markdown("<h1 style='text-align: center; font-family: Open Sans, sans-serif;'>生物単語ガチャ</h1>", unsafe_allow_html=True)
css = """
h1 {
    color: #00CED1; /* タイトルの文字色を赤に変更 */
}
"""

# CSSを適用する
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
st.write('生物用語をランダムに表示して、勉強をサポートします！')
st.write('がんばってください！')

# Load the data
@st.cache
def load_data():
    return pd.read_excel("生物ガチャ.xlsx")

words_df = load_data()

# ガチャ機能
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.markdown('<div style="display: flex; justify-content: center;">'
                '<button style="width: 200px; height: 50px;" onclick="window.location.reload();">ガチャを引く！</button>'
                '</div>', unsafe_allow_html=True)

if 'selected_word' in st.session_state:
    st.title(f"Q: {st.session_state.selected_word['説明']}")

    # 正解と誤答を取得
    correct_answer = st.session_state.selected_word['単語']
    wrong_answers = words_df[words_df['レア度'] != st.session_state.selected_word['レア度']]['単語'].tolist()

    # 正解を含む選択肢をランダムに選ぶ
    options = random.sample(wrong_answers, 3) + [correct_answer]

    # 選択肢をシャッフル
    random.shuffle(options)

    # 解答選択肢を表示
    user_answer = st.radio("解答を選択してください", options)

    # 解答が正しいかどうかを確認し、結果を表示
    if user_answer.strip() == str(correct_answer):
        st.write("正解です！")
    else:
        st.write("不正解です。正しい答えは", correct_answer, "です。")

    # 正解と解答を表示
    st.write(f"正しい答え: {correct_answer}")
    st.write(f"あなたの答え: {user_answer}")
