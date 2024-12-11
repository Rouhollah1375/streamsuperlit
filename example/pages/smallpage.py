from components.SmallComponent import small_cmp
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import datetime

st_autorefresh(interval= 1 * 1000, key="dataframerefresh")


st.header('Small Page')
st.text(datetime.datetime.now())

small_cmp()