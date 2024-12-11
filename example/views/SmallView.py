from streamsuperlit.view import View
from streamsuperlit.core.lifecycle_hook import AfterInit

import streamlit as st

class SmallView(View, AfterInit):
    def __new__(cls, id: str):
        return super(SmallView, cls).__new__(cls, id)

    def __init__(self, id: str):
        super().__init__(id)

    def after_init(self):
        pass
        
    def _view(self):
        st.text('hello')
        st.button('click me', on_click=self._ctrl.increment)
        st.text(self._ctrl.get_a())