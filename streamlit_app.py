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

# Load the data
@st.cache_data
def load_data():
    return pd.read_excel("生物ガチャ.xlsx")

words_df = load_data()

# 初期点数の設定
if 'score' not in st.session_state:
    st.session_state.score = 0

# 制限時間（秒）
quiz_timeout_duration = 10

def clear_feedback():
    if 'feedback_container' in st.session_state:
        st.session_state.feedback_container.empty()

# ガチャ機能
if st.button('ガチャを引く！'):
    # ガチャボタンを押した時点で正解・不正解のメッセージを非表示にする
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
st.sidebar.write(f"現在の点数: {st.session_state.score}")

# クイズの表示
if 'selected_word' in st.session_state:
    st.header("説明")
    st.write(st.session_state.selected_word['説明'])
    st.subheader(f"レア度: {st.session_state.selected_word['レア度']}")

    # 残り時間の計算と表示
    start_time = st.session_state.start_time
    time_container = st.empty()  # 時間を表示するための空のコンテナ

    # タイマーの初期化
    remaining_time = quiz_timeout_duration
    
    if not st.session_state.quiz_answered:
        # 選択肢を表示
        quiz_answer = st.radio("選択肢", st.session_state.choices)
        
        if st.button('解答する'):
            st.session_state.quiz_answered = True
            st.session_state.selected_choice = quiz_answer

    # タイマーのループ
    while not st.session_state.quiz_answered and remaining_time > 0:
        elapsed_time = time.time() - start_time
        remaining_time = max(quiz_timeout_duration - elapsed_time, 0)
        
        # タイマーの表示を更新
        time_container.write(f"残り時間: {int(remaining_time)}秒")
        time.sleep(0.1)  # 0.1秒ごとに更新

    # 時間切れの処理
    if not st.session_state.quiz_answered and remaining_time <= 0:
        st.warning("時間切れです。もう一度ガチャを引いてください。")
        clear_feedback()  # 時間切れ時にフィードバックをクリア
        st.session_state.choices = []  # 空のリストにして選択肢を非表示

    # クイズが解答された後、結果を表示
    if st.session_state.quiz_answered:
        feedback_container = st.empty()
        if st.session_state.selected_choice == st.session_state.correct_answer:
            st.session_state.score += 10  # 正解の場合に点数を追加
            feedback_container.success("正解です！")
        else:
            feedback_container.error(f"不正解です。")
            st.write(f"正解は {st.session_state.correct_answer}")            
        
        # 解答後にフィードバックをクリア
        st.session_state.feedback_container = feedback_container

        # 次の問題に移った時にフィードバックを非表示にする
        st.session_state.quiz_answered = False
