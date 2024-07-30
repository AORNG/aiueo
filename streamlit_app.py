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

col1,col2 = st.columns(2)

# ガチャ機能
with col1:
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

    with col2:
        if st.button("スコアリセット"):
            st.session_state.score = 0

    # クイズの表示と処理
    if 'selected_word' in st.session_state:
        st.write("説明")
        st.header(st.session_state.selected_word['説明'])
        st.subheader(f"レア度: {st.session_state.selected_word['レア度']}")

        # タイマーの表示と回答選択肢の表示
        start_time = st.session_state.start_time
        elapsed_time = time.time() - start_time
        remaining_time = max(quiz_timeout_duration - elapsed_time, 0)
        time_container = st.empty()  # 時間を表示するための空のコンテナ
        time_container.title(f"残り時間: {int(remaining_time)} 秒")

        if not st.session_state.quiz_answered:
            # 解答選択肢をチェックボックスで表示
            checked = [False] * len(st.session_state.choices)
            checked[0] = st.checkbox(st.session_state.choices[0])
            checked[1] = st.checkbox(st.session_state.choices[1])
            checked[2] = st.checkbox(st.session_state.choices[2])
            checked[3] = st.checkbox(st.session_state.choices[3])

            # 解答ボタンの表示と処理
            if not st.session_state.answer_button_disabled and any(checked):
                if st.button('解答する'):
                    st.session_state.quiz_answered = True
                    st.session_state.answer_button_disabled = True  # 解答ボタンを無効化
                    
                    # チェックされた選択肢を判定
                    selected_choices = [choice for i, choice in enumerate(st.session_state.choices) if checked[i]]
                    if st.session_state.correct_answer in selected_choices:
                        st.session_state.score += 10
                        st.success("正解です！")
                    else:
                        st.session_state.score = max(st.session_state.score - 10, 0)
                        st.error("不正解です。")
                        st.write(f"正解は {st.session_state.correct_answer}")

        # タイマーの更新（1秒ごと）
        while remaining_time > 0 and not st.session_state.quiz_answered:
            elapsed_time = time.time() - st.session_state.start_time
            remaining_time = max(quiz_timeout_duration - elapsed_time, 0)
            time_container.title(f"残り時間: {int(remaining_time)} 秒")
            time.sleep(1)  # 1秒待つ

        # 残り時間が0になった場合の処理
        if remaining_time == 0:
            st.session_state.quiz_answered = True
            st.session_state.answer_button_disabled = True
