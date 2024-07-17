import streamlit as st
import pandas as pd
import numpy as np
import time

# Page title with styled CSS
st.markdown("<h1 style='text-align: center; color: #00CED1; font-family: Open Sans, sans-serif;'>生物単語ガチャ</h1>", unsafe_allow_html=True)

# Introduction texts
st.write('生物用語をランダムに表示して、勉強をサポートします！')
st.write('がんばってください！')

# Load data from Excel file
@st.cache
def load_data():
    return pd.read_excel("生物ガチャ.xlsx")

words_df = load_data()

# Initialize score if not in session state
if 'score' not in st.session_state:
    st.session_state.score = 0

# Initialize quiz answered state
if 'quiz_answered' not in st.session_state:
    st.session_state.quiz_answered = False

# Initialize answer button state
if 'answer_button_disabled' not in st.session_state:
    st.session_state.answer_button_disabled = False

# Gacha function
if st.button('ガチャを引く！'):
    st.session_state.feedback_container = None  # Clear previous feedback
    rarity_probs = {'N': 0.4, 'R': 0.3, 'SR': 0.2, 'SSR': 0.1}
    chosen_rarity = np.random.choice(list(rarity_probs.keys()), p=list(rarity_probs.values()))
    subset_df = words_df[words_df['レア度'] == chosen_rarity]
    selected_word = subset_df.sample().iloc[0]
    
    # Generate quiz choices
    other_words = words_df[words_df['説明'] != selected_word['説明']].sample(3)
    choices = other_words['単語'].tolist() + [selected_word['単語']]
    np.random.shuffle(choices)
    
    # Save selected word and choices to session state
    st.session_state.selected_word = selected_word
    st.session_state.choices = choices
    st.session_state.correct_answer = selected_word['単語']
    st.session_state.display_meaning = False
    st.session_state.quiz_answered = False
    st.session_state.start_time = time.time()  # Record quiz start time
    st.session_state.answer_button_disabled = False  # Enable answer button

# Display current score in sidebar
st.sidebar.header("スコア")
st.sidebar.markdown(f"<h2 style='font-size: 2em; text-align: center;'>現在の点数: {st.session_state.score}</h2>", unsafe_allow_html=True)

# Quiz display section
if 'selected_word' in st.session_state:
    st.write("説明")
    st.header(st.session_state.selected_word['説明'])
    st.subheader(f"レア度: {st.session_state.selected_word['レア度']}")

    # Initialize timer
    start_time = st.session_state.start_time
    time_container = st.empty()  # Container for timer display

    # Timer loop
    while not st.session_state.quiz_answered:
        elapsed_time = time.time() - start_time
        remaining_time = max(10 - elapsed_time, 0)  # Quiz timeout duration
        
        # Update timer display
        time_container.write(f"残り時間: {int(remaining_time)}秒")
        
        if remaining_time <= 0:
            # Timeout handling
            st.warning("時間切れです。もう一度ガチャを引いてください。")
            st.session_state.choices = []  # Hide choices
            break
        
        time.sleep(0.1)  # Update every 0.1 second

        # Disable answer button when time runs out
        if remaining_time == 0:
            st.session_state.quiz_answered = True
            st.session_state.answer_button_disabled = True

        # Display choices
        if not st.session_state.quiz_answered:
            quiz_answer = st.radio(f"選択肢_{start_time}", st.session_state.choices)
        
            if not st.session_state.answer_button_disabled:
                if st.button('解答する'):
                    st.session_state.quiz_answered = True
                    st.session_state.selected_choice = quiz_answer
                    st.session_state.answer_button_disabled = True  # Disable answer button

    # Post-quiz processing
    if st.session_state.quiz_answered:
        time_container.empty()  # Hide timer display
        
        # Display result feedback
        if st.session_state.selected_choice == st.session_state.correct_answer:
            st.session_state.score += 10  # Add score for correct answer
            st.success("正解です！")
        else:
            st.error(f"不正解です。正解は {st.session_state.correct_answer}")
            st.session_state.score = max(st.session_state.score - 10, 0)  # Deduct score for incorrect answer
        
        st.session_state.quiz_answered = False  # Reset quiz answered state

# Disable answer button if quiz is already answered
if st.session_state.quiz_answered:
    st.button('解答する', disabled=True)

# Score reset button
if st.button("スコアリセット"):
    st.session_state.score = 0
