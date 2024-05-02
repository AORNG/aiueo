import streamlit as st
import random

def main():
    st.title('くじ引きアプリ')

    user_name=st.text_input(名前を入力)

    # くじのリストを定義
    kuji_list = ['大吉', '中吉', '小吉', '凶', '大凶']

    # くじを引くためのボタン
    if st.button('くじを引く'):
        # くじ引きの結果をランダムに選択
        result = random.choice(kuji_list)
        comments={
            "大吉":"すごい"
        }
        comment=comments[result]
        st.write(f'結果: {result}')

if __name__ == '__main__':
    main()
