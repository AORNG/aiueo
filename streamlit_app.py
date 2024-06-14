if 'selected_word' in st.session_state:
    st.title(f"Q: {st.session_state.selected_word['説明']}")

    # 正解と誤答を取得
    correct_answer = st.session_state.selected_word['単語']
    wrong_answers = words_df[words_df['レア度'] != st.session_state.selected_word['レア度']]['単語'].tolist()

    # 解答選択肢を表示
    st.write("解答:")
    st.write(correct_answer)

    # 解答選択肢を表示せずに解答を直接表示
    st.write("答え合わせボタンを押して正解を確認してください。")
