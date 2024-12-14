import streamlit as st

a = 0
def increment():
    global a
    a += 1

st.button('increment', on_click=increment)
st.text(f'Current value of a: {a}')