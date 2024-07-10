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
@st.cache(allow_output_mutation=True)
def load_data():
    return pd.read_excel("生物ガチャ.xlsx")

words_df = load_data()

# 制限時間（秒）
quiz_timeout_duration = 10

# セッションステートにスコアを追加
if 'score' not in st.session_state:
    st.session_state.score = 0

def clear_feedback():
    if 'feedback_container' in st.session_state:
        st.session_state.feedback_container.empty()

# スタートボタンとスコアリセットの処理
if not st.session_state.get('started', False):
    if st.button("スタート"):
        st.session_state.started = True
        st.session_state.score = 0
        st.session_state.answer_submitted = False
        st.session_state.quiz_answered = False
        st.session_state.selected_word = None
        st.session_state.choices = []

# ガチャ機能
if st.session_state.get('started', False):
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
        st.session_state.answer_submitted = False  # 解答が送信されたかどうかのフラグ
        st.session_state.start_time = time.time()  # クイズの開始時刻を記録

    if st.session_state.selected_word is not None:
        st.header(f"説明")
        st.header(f"{st.session_state.selected_word['説明']}")
        st.subheader(f"レア度: {st.session_state.selected_word['レア度']}")

        # 残り時間の計算と表示
        elapsed_time = time.time() - st.session_state.start_time
        remaining_time = max(quiz_timeout_duration - elapsed_time, 0)
        
        # 残り時間を更新
        st.session_state.remaining_time = int(remaining_time)

        if remaining_time <= 0:
            st.warning("時間切れです。もう一度ガチャを引いてください。")
            clear_feedback()  # 時間切れ時にフィードバックをクリア

        if remaining_time > 0 and not st.session_state.answer_submitted:
            # クイズを表示
            quiz_answer = st.radio("選択肢", st.session_state.choices)
            
            if st.button('解答する'):
                st.session_state.answer_submitted = True  # 解答が送信されたことをフラグで管理
                st.session_state.selected_choice = quiz_answer

                # セッションステートのタイマーを更新
                st.session_state.timer_update = time.time()

        # クイズが解答された後、結果を表示
        if st.session_state.answer_submitted:
            feedback_container = st.empty()
            if st.session_state.selected_choice == st.session_state.correct_answer:
                feedback_container.success("正解です！")
                st.session_state.score += 1  # 正解したら得点を加算
            else:
                feedback_container.error(f"不正解です。")
                st.write(f"正解は {st.session_state.correct_answer}")            
            
            # 解答後にフィードバックをクリア
            st.session_state.feedback_container = feedback_container

            # 次の問題に移った時にフィードバックを非表示にする
            st.session_state.answer_submitted = False  # 解答が送信されたフラグをリセット

    # 残り時間の表示
    st.write(f"残り時間: {st.session_state.remaining_time}秒")

    # 得点を大きく表示
    st.markdown(f"<h2 style='text-align: center;'>得点: {st.session_state.score}</h2>", unsafe_allow_html=True)
