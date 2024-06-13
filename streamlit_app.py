import streamlit as st

def main():
    st.title("解答確認アプリ")

    # 問題を表示
    question = "2 + 2 は？"
    st.write("問題:", question)

    # 解答欄を作成
    user_answer = st.text_input("解答を入力してください")

    # 解答合わせボタン
    if st.button("答え合わせ"):
        correct_answer = 4  # 正解を定義

        # 解答が正しいかどうかを確認し、結果を表示
        if user_answer.strip() == str(correct_answer):
            st.success("正解です！正しい答えは" + str(correct_answer) + "です。")  # 成功メッセージを表示
        else:
            st.error("不正解です。正しい答えは" + str(correct_answer) + "です。")  # エラーメッセージを表示

if __name__ == "__main__":
    main()
