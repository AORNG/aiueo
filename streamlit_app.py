import streamlit as st
import pandas as pd
import numpy as np
import time

timeout_duration = 10
start_time = time.time()

while True:
    current_time = time.time()
    current_time = time.time()
    elapsed_time = current_time - start_time

        # 制限時間を超えた場合はアプリケーションを停止
    if elapsed_time > timeout_duration:
        st.error(f'Timeout: Application closed after {timeout_duration} seconds.')
        break

        # ここにアプリケーションのコンテンツを追加する
    st.write(f"Elapsed Time: {int(elapsed_time)} seconds")
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

        timeout_duration = 10
        start_time = time.time()
        
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

    if 'selected_word' in st.session_state:
        st.header(f"説明")
        st.header(f"{st.session_state.selected_word['説明']}")
        st.subheader(f"レア度: {st.session_state.selected_word['レア度']}")

        # クイズを表示
        quiz_answer = st.radio("選択肢", st.session_state.choices)
        
        if st.button('解答する'):
            st.session_state.quiz_answered = True
            st.session_state.selected_choice = quiz_answer

        if st.session_state.quiz_answered:
            if st.session_state.selected_choice == st.session_state.correct_answer:
                st.success("正解です！")
            else:
                st.error("不正解です。")
                st.write(f"正解は {st.session_state.correct_answer}")