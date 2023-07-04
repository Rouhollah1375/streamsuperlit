import streamlit as st
from abc import ABC, abstractmethod

class Model(ABC):
    def __new__(cls, id: str):
        if id not in st.session_state:
            st.session_state[id] = super(Model, cls).__new__(cls)
        return st.session_state[id]

    def __init__(self, id: str):
        self._id = id

