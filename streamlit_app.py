import streamlit as st

st.title("BMI計算アプリ")
st.text("体重を入力してください")

weight=st.number_input("体重を入力(kg)")

st.write("あなたの体重は"+str(weight)+"kgです")
a=weight-10

st.write(str(a)+"kgを目指しましょう")

st.text("身長を入力してください")

long=st.number_input("身長を入力(m)")

st.write("あなたの身長は"+str(weight)+"mです")
b=long+0.1

st.write(str(b)+"mを目指しましょう")
if st.button("計算"):

c=weight/long**2
st.text(c)