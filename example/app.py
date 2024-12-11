import os, sys

DEBUG = True
if DEBUG:
    os.system('pip uninstall -y streamsuperlit')       # removing the stable version
    sys.path.append('../src')                      # adding the development version
else:
    os.system('pip uninstall -y streamsuperlit')       # removing the stable version
    os.system('pip install -r requirements.txt')

from streamsuperlit.utils import navigate
import streamlit as st

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    navigate('main_page')