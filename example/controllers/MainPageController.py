from streamsuperlit.controller import Controller
from streamsuperlit.core.lifecycle_hook import OnInit
import streamlit as st
import pandas as pd

class MainPageController(Controller, OnInit):

    def handle_button_click(self):
        self._view.a += 1
        self._view.b = 'even' if self._view.a % 2 == 0 else 'odd'
    
    def is_email(self):
        print(st.session_state)
        email = st.session_state[self._view._id+'3']
        self._view.is_email = '@' in email

    def on_init(self):
        self._df = pd.DataFrame({
            'id': ['asdf', 'ert', 'vb', 'ty', 'ewtty'],
            'balance': [1, 123, -1, 45, 89],
        })

    def get_df(self) -> pd.DataFrame:
        return self._df