import streamlit as st
import random

st.title("歴史単語ガチャ")
st.write ("歴史に強くなりましょう！")
a = ["2020年から流行ったウイルスの名前は何か？"]
b = ["1939年9月1日に起こったことは何か？"]
c = ["2020年から流行ったウイルスの名前は何か？","1939年9月1日に起こったことは何か？"]
c = random.choice("a","b")
d = ["新型コロナウイルス"]
e = ["第二次世界大戦"]
k = ["新型コロナウイルス","第二次世界大戦"]
g = random.choice(k)
if st.button("勉強を開始する"):
   st.write(f"問題:{c}")
   if st.button("解答を見る"):
      st.write(f"解答:{g}")