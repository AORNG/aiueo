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
.button-center {
    display: block;
    margin: 0 auto;
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

# スコアの初期化
if 'score' not in st.session_state:
    st.session_state.score = 0

# クイズの回答状態を管理する変数
if 'quiz_answered' not in st.session_state:
    st.session_state.quiz_answered = False

words_df = load_data()

# 制限時間（秒）
quiz_timeout_duration = 10

def clear_feedback():
    if 'feedback_container' in st.session_state:
        st.session_state.feedback_container.empty()

# ガチャ機能
if st.button('ガチャを引く！', key='gacha_button'):
    # ガチャボタンを押したときに点数をリセットしないように修正
    clear_feedback()
    
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

# 点数の表示
st.sidebar.header("スコア")
st.sidebar.markdown(f"<h2 style='font-size: 2em; text-align: center;'>現在の点数: {st.session_state.score}</h2>", unsafe_allow_html=True)

# クイズの表示
if 'selected_word' in st.session_state:
    st.write("説明")
    st.header(st.session_state.selected_word['説明'])
    st.subheader(f"レア度: {st.session_state.selected_word['レア度']}")

    # タイマーの初期化
    start_time = st.session_state.start_time
    time_container = st.empty()  # 時間を表示するための空のコンテナ

    if not st.session_state.quiz_answered:
        # 選択肢の表示
        quiz_answer = st.radio("選択肢", st.session_state.choices)
        
        if st.button('解答する', key='answer_button'):
            st.session_state.quiz_answered = True
            st.session_state.selected_choice = quiz_answer

    # クイズが解答された後の処理
    if st.session_state.quiz_answered:
        # タイマーを非表示にするために空のコンテナを利用
        time_container.empty()

        # 結果を表示
        feedback_container = st.empty()
        if st.session_state.selected_choice == st.session_state.correct_answer:
            st.session_state.score += 10  # 正解の場合に点数を追加
            feedback_container.success("正解です！")
        else:
            feedback_container.error(f"不正解です。")
            st.write(f"正解は {st.session_state.correct_answer}")
            st.session_state.score = max(st.session_state.score - 10, 0)  # 不正解の場合に点数を減らす
        
        # 解答後にフィードバックをクリア
        st.session_state.feedback_container = feedback_container

        # 次の問題に移った時にフィードバックを非表示にする
        st.session_state.quiz_answered = False

# 回答がある場合は回答ボタンを無効化する
if st.session_state.quiz_answered:
    st.button('解答する', key='answer_button', disabled=True)
