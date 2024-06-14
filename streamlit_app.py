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
if st.button('ガチャを引く！'):
    rarity_probs = {
        'N': 0.4,
        'R': 0.3,
        'SR': 0.2,
        'SSR': 0.1
    }
    chosen_rarity = np.random.choice(list(rarity_probs.keys()), p=list(rarity_probs.values()))
    subset_df = words_df[words_df['レア度'] == chosen_rarity]
    selected_word = subset_df.sample().iloc[0]
    
    # クイズ用の選択肢を生成
    other_words = words_df[words_df['用語'] != selected_word['用語']].sample(2)
    choices = other_words['用語の意味'].tolist() + [selected_word['用語の意味']]
    np.random.shuffle(choices)
    
    # セッションステートに選択された単語とクイズ選択肢を保存
    st.session_state.selected_word = selected_word
    st.session_state.choices = choices
    st.session_state.correct_answer = selected_word['用語の意味']
    st.session_state.display_meaning = False
    st.session_state.quiz_answered = False

if 'selected_word' in st.session_state:
    st.header(f"用語名: {st.session_state.selected_word['用語']}")
    st.subheader(f"難易度: {st.session_state.selected_word['難易度']}")

    # クイズを表示
    st.write("この用語の意味はどれでしょう？")
    quiz_answer = st.radio("選択肢", st.session_state.choices)
    
    if st.button('回答する'):
        st.session_state.quiz_answered = True
        st.session_state.selected_choice = quiz_answer

    if st.session_state.quiz_answered:
        if st.session_state.selected_choice == st.session_state.correct_answer:
            st.success("正解です！")
        else:
            st.error("不正解です。")
        st.write(f"正しい意味: {st.session_state.correct_answer}")