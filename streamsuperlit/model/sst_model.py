from streamsuperlit.model import Model
import streamlit as st

class SSTModel(Model):
    id = 'sst-model'
    def __new__(cls):
        if id not in st.session_state:
            st.session_state[SSTModel.id] = super(SSTModel, cls).__new__(cls, SSTModel.id)
        return st.session_state[SSTModel.id]

    def __init__(self):
        self.views = {}
        self.controllers = {}
        super().__init__(SSTModel.id)

    def register_view(self, view: 'streamsuperlit.view.View'):
        self.views[id(view)] = view

    def register_controller(self, controller: 'streamsuperlit.controller.Controller'):
        self.controllers[id(controller)] = controller
    