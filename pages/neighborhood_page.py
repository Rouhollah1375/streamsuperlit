import streamlit as st
import pandas as pd
from nav_page import nav_page

def back_to_home():
    nav_page('app')

if 'neighoborhood_name' in st.session_state.keys():
    neigh, df = st.session_state['neighoborhood_name'], st.session_state['neighoborhood_df']
else:
    st.write('Error - state is not properly set.')



st.button('main page', on_click=back_to_home)
