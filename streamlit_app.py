import streamlit as st
import pandas as pd
import numpy as np
import openpyxl
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
    
    # セッションステートに選択された単語を保存
    st.session_state.selected_word = selected_word
    st.session_state.display_meaning = False

if 'selected_word' in st.session_state:
    st.title(f"Q: {st.session_state.selected_word['説明']}")

    # 正解と誤答を取得
    correct_answer = st.session_state.selected_word['単語']
    wrong_answers = words_df[words_df['レア度'] != st.session_state.selected_word['レア度']]['単語'].sample(n=3).tolist()
    options = [correct_answer] + wrong_answers
    random.shuffle(options)

    # 解答選択肢を表示import streamlit as st
import pandas as pd
import numpy as np
import openpyxl
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
    
    # セッションステートに選択された単語を保存
    st.session_state.selected_word = selected_word
    st.session_state.display_meaning = False

if 'selected_word' in st.session_state:
    st.title(f"Q: {st.session_state.selected_word['説明']}")

    # 正解と誤答を取得
    correct_answer = st.session_state.selected_word['単語']
    wrong_answers = words_df[words_df['レア度'] != st.session_state.selected_word['レア度']]['単語'].tolist()
    options = [correct_answer] + random.sample(wrong_answers, min(3, len(wrong_answers)))

    # 解答選択肢を表示
    user_answer = st.radio("解答を選択してください", options)

    # 答え合わせボタン
    if st.button("答え合わせ"):
        # 解答が正しいかどうかを確認し、結果を表示
        if user_answer.strip() == str(correct_answer):
            st

    user_answer = st.radio("解答を選択してください", options)

    # 答え合わせボタン
    if st.button("答え合わせ"):
        # 解答が正しいかどうかを確認し、結果を表示
        if user_answer.strip() == str(correct_answer):
            st.write("正解です！")
        else:
            st.write("不正解です。正しい答えは", correct_answer, "です。")
