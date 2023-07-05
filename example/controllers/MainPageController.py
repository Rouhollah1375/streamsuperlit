from streamsuperlit.controller import Controller
import streamlit as st

class MainPageController(Controller):

    def handle_button_click(self):
        self._view.a += 1
        self._view.b = 'even' if self._view.a % 2 == 0 else 'odd'
    
    def is_email(self):
        print(st.session_state)
        email = st.session_state[self._view._id+'3']
        self._view.is_email = '@' in email