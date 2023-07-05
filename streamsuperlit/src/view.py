from abc import abstractmethod, ABC
from collections.abc import Callable
import streamlit as st
import datetime
import streamlit as st

class View(ABC):
    def __new__(cls, id: str):
        if id not in st.session_state:
            st.session_state[id] = super(View, cls).__new__(cls)
        return st.session_state[id]

    def __init__(self, id: str):
        self._id = id
        self._inputs: list[object] = []
        self._outputs: list[Callable] = []

    def _handle_outputs(self):
        pass

    def _handle_inputs(self):
        pass

    def register_controller(self, controller: 'streamsuperlit.controller.Controller'):
        self._ctrl = controller

    def render(self):
        self._handle_outputs()
        self._handle_inputs()
        self._view()

    @abstractmethod
    def _view(self):
        pass

    def register_output(self, func: Callable):
        self._outputs.append(func)
