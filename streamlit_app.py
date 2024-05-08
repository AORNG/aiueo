import streamlit as st

st.title("BMI計算アプリ")
st.text("体重を入力してください")

weight=st.number_input("体重を入力")

st.write("あなたの体重は"+str(weight)+"kgです")
a=weight-10

st.write(str(a)+"kgを目指しましょう")

st.text("身長を入力してください")

long=st.number_input("身長を入力")

st.write("あなたの身長は"+str(weight+"cmです"))
b=long+10

st.write(str(b)+"cmを目指しましょう")