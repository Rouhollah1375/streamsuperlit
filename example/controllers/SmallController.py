from streamsuperlit.controller import Controller
from streamsuperlit.core.lifecycle_hook import OnInit

import streamlit as st

class SmallController(Controller, OnInit):
    def on_init(self):
        self.a = 0

    def increment(self):
        print('hello')
        self.a += 1

    def get_a(self):
        return self.a

def get_params():
    return st.experimental_get_query_params()
