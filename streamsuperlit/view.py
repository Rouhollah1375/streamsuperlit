from abc import abstractmethod, ABC
from collections.abc import Callable
import streamlit as st
import datetime
import streamlit as st

class View(ABC):
    def __new__(cls, id: str, controller: 'streamsuperlit.controller.Controller'):
        if id not in st.session_state:
            st.session_state[id] = super(View, cls).__new__(cls)
        return st.session_state[id]

    def __init__(self, id: str, controller: 'streamsuperlit.controller.Controller'):
        self._id = id
        self._ctrl = controller
        self._ctrl.register_view(self)
        self._inputs: list[object] = []
        self._outputs: list[Callable] = []

    def _handle_outputs(self):
        pass

    def _handle_inputs(self):
        pass

    def render(self):
        self._handle_outputs()
        self._handle_inputs()
        self._view()

    @abstractmethod
    def _view(self):
        pass

    def register_output(self, func: Callable):
        self._outputs.append(func)
