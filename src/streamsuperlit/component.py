from streamsuperlit.view import View
from streamsuperlit.controller import Controller
import streamlit as st

class Component:
    def __new__(cls, name: str, id: str,
                    view_cls: View.__class__,
                    controller_cls: Controller.__class__):
                    if id not in st.session_state:
                        st.session_state[id] = super(Component, cls).__new__(cls)
                    return st.session_state[id]
    def __init__(self, name: str, id: str,
                    view_cls: View.__class__,
                    controller_cls: Controller.__class__) -> None:
        self._name = name
        self._id = id
        self._view: View = view_cls(f'{id}-view')
        self._controller: Controller = controller_cls(f'{id}-controller')

        self._view.register_controller(self._controller)
        self._controller.register_view(self._view)

    def get_view(self):
        return self._view