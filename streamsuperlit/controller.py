from streamsuperlit.view import View
import streamlit as st

class Controller:
    def __new__(cls, id: str, sst_model: 'streamsuperlit.model.SSTModel'):
        if id not in st.session_state:
            st.session_state[id] = super(Controller, cls).__new__(cls)
        return st.session_state[id]

    def __init__(self, id: str, sst_model: 'streamsuperlit.model.SSTModel'):
        self._id = id
        sst_model.register_controller(self)

    def register_view(self, view: View):
        self._view = view