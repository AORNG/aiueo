import streamlit as st
import pandas as pd
import numpy as np

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
@st.cache_resource
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
# 説明を確認するボタンを追加
if 'selected_word' in st.session_state:
    if st.button('問題の表示'):
        st.session_state.display_meaning = True
        if st.session_state.display_meaning:
            st.write(f"問題: {st.session_state.selected_word['説明']}")
            def main():
                st.title("解答入力")

            # テキストボックスを表示してユーザーに解答を入力させる
            answer = st.text_input("解答を入力してください")

            # 入力された解答を表示
            st.write("入力された解答:", answer)

        if __name__ == "__main__":
            main()

    st.header(f"単語名: {st.session_state.selected_word['単語']}")
    st.subheader(f"レア度: {st.session_state.selected_word['レア度']}")

    