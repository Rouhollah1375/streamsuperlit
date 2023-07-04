import streamlit as st

class Controller:
    def __new__(cls, id: str):
        if id not in st.session_state:
            st.session_state[id] = super(Controller, cls).__new__(cls)
        return st.session_state[id]

    def __init__(self, id: str):
        self._id = id

    def register_view(self, view: 'streamsuperlit.view.View'):
        self._view = view