import streamlit as st
import pandas as pd
import numpy as np
import time

# タブの選択
tab_selection = st.sidebar.radio("高1", ["第一章、第二章", "第三章、第四章"])

# Montserratフォントを使ったタイトルを表示
st.markdown("<h1 style='text-align: center; font-family: Open Sans, sans-serif; color: #00CED1;'>生物単語ガチャ</h1>", unsafe_allow_html=True)
st.write('生物用語をランダムに表示して、勉強をサポートします！')
st.write('がんばってください！')

# CSS
css = """
h1 {
    color: #00CED1; /* タイトルの文字色を変更 */
    text-align: center;
    font-family: Open Sans, sans-serif;
}
"""
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# データの読み込み（Excelファイルの読み込みをサンプルとしています）
@st.cache
def load_data():
    return pd.read_excel("生物ガチャ.xlsx")

# スコアの初期化とセッション状態の管理
if 'score' not in st.session_state:
    st.session_state.score = 0

# データを読み込む
words_df = load_data()

# 制限時間（秒）
quiz_timeout_duration = 10

# クイズを表示するためのトグルボタン
show_quiz = st.button("ガチャを引く！")

if show_quiz:
    # フィードバックをクリア
    st.session_state.quiz_answered = False
    st.session_state.answer_button_disabled = False
    
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
    st.session_state.start_time = time.time()  # クイズの開始時刻を記録

    # クイズの表示と処理
    st.write("説明")
    st.header(st.session_state.selected_word['説明'] + f"[レア度: {st.session_state.selected_word['レア度']}]")
    
    # 解答選択肢をボタン形式で表示
    for choice in st.session_state.choices:
        if st.button(choice):
            st.session_state.selected_choice = choice
    
    # タイマーの表示と回答選択肢の表示
    start_time = st.session_state.start_time
    elapsed_time = time.time() - start_time
    remaining_time = max(quiz_timeout_duration - elapsed_time, 0)
    time_container = st.empty()  # 時間を表示するための空のコンテナ
    time_container.title(f"残り時間: {remaining_time:.1f} 秒")

    # 解答ボタンの表示と処理
    if not st.session_state.answer_button_disabled:
        if st.button('解答する'):
            st.session_state.quiz_answered = True
            st.session_state.answer_button_disabled = True  # 解答ボタンを無効化
            
            # 正誤判定とフィードバックの表示
            selected_choice = st.session_state.selected_choice
            if selected_choice == st.session_state.correct_answer:
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
        time_container.title(f"残り時間: {remaining_time:.1f} 秒")
        time.sleep(0.1)  # 0.1秒待つ

    # 残り時間が0になった場合の処理
    if remaining_time == 0:
        st.session_state.quiz_answered = True
        st.session_state.answer_button_disabled = True

# スコアの表示
st.sidebar.header("スコア")
st.sidebar.markdown(f"<h2 style='font-size: 2em; text-align: center;'>現在の点数: {st.session_state.score}</h2>", unsafe_allow_html=True)   

# スコアリセットボタンの処理
if st.sidebar.button("スコアリセット"):
    st.session_state.score = 0

# ガチャタブのコンテンツ
if tab_selection == "第一章、第二章":
    st.write("第一章、第二章")
