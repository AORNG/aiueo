import streamlit as st
import pandas as pd
import numpy as np
import time

# Montserratフォントを使ったタイトルを表示
st.markdown("<h1 style='text-align: center; font-family: Open Sans, sans-serif;'>生物単語ガチャ</h1>", unsafe_allow_html=True)
css = """
h1 {
    color: #00CED1; /* タイトルの文字色を変更 */
}
"""

# CSSを適用する
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
st.write('生物用語をランダムに表示して、勉強をサポートします！')
st.write('がんばってください！')

# データの読み込み（Excelファイルの読み込みをサンプルとしています）
@st.cache
def load_data():
    return pd.read_excel("生物ガチャ.xlsx")

# スコアの初期化とセッション状態の管理
if 'score' not in st.session_state:
    st.session_state.score = 0

if 'quiz_answered' not in st.session_state:
    st.session_state.quiz_answered = False

if 'answer_button_disabled' not in st.session_state:
    st.session_state.answer_button_disabled = False

# データを読み込む
words_df = load_data()

# 制限時間（秒）
quiz_timeout_duration = 10

# フィードバックコンテナをクリアする関数
def clear_feedback():
    if 'feedback_container' in st.session_state:
        st.session_state.feedback_container.empty()

# ガチャ機能
if st.button('ガチャを引く！'):
    clear_feedback()  # フィードバックをクリア
    
    # レア度ごとの確率設定
    rarity_probs = {
        'N': 0.4,
        'R': 0.3,
        'SR': 0.2,
        'SSR': 0.1
    }
    
    # レア度に応じて単語を選択
    chosen_rarity = np.random.choice(list(rarity_probs.keys()), p=list(rarity_probs.values()))
    subset_df = words_df[words_df['レア度'] == chosen_rarity]
    selected_word = subset_df.sample().iloc[0]
    
    # クイズ用の選択肢を生成
    other_words = words_df[words_df['説明'] != selected_word['説明']].sample(3)
    choices = other_words['単語'].tolist() + [selected_word['単語']]
    np.random.shuffle(choices)
    
    # セッションステートに選択された単語とクイズ選択肢を保存
    st.session_state.selected_word = selected_word
    st.session_state.choices = choices
    st.session_state.correct_answer = selected_word['単語']
    st.session_state.display_meaning = False
    st.session_state.quiz_answered = False
    st.session_state.start_time = time.time()  # クイズの開始時刻を記録
    st.session_state.answer_button_disabled = False  # 解答ボタンを有効化

# スコアの表示とリセット
st.sidebar.header("スコア")
st.sidebar.markdown(f"<h2 style='font-size: 2em; text-align: center;'>現在の点数: {st.session_state.score}</h2>", unsafe_allow_html=True)

if st.button("スコアリセット"):
    st.session_state.score = 0

# クイズの表示と処理
if 'choices' in st.session_state:
    if st.button(st.session_state.choices[0]):
        # Handle button click logic here
        pass  # Placeholder for your logic
