from streamsuperlit.model import Model
from streamsuperlit.view import View
from streamsuperlit.controller import Controller
from streamsuperlit.component import Component
from streamsuperlit.core.uuid import UUID
from streamsuperlit.core.utils import get_class
from collections import OrderedDict

import streamlit as st

class SSTCore(Model):
    SSTCORE_ID = 'sst-core'
    def __new__(cls, components: list[dict]):
        if SSTCore.SSTCORE_ID not in st.session_state:
            st.session_state[SSTCore.SSTCORE_ID] = super(SSTCore, cls).__new__(cls, SSTCore.SSTCORE_ID)
            st.session_state['core-init'] = False
        return st.session_state[SSTCore.SSTCORE_ID]

    def __init__(self, components: list[dict]):
        if not st.session_state['core-init']:
            self._components = OrderedDict()
            self._uuid = UUID()
            self.build_components(components)
            st.session_state['core-init'] = True

        super().__init__(SSTCore.SSTCORE_ID)
    
    def create_component(self, name: str, view_cls: str, controller_cls: str):
        id = self._uuid.get_uuid()
        try:
            view_class = get_class(view_cls)
            controller_class = get_class(controller_cls)
        except:
            raise Exception(f'Cannot create the component {name}. view_cls or controller_cls are not properly provided.')
        self._components[id] = Component(name, id, view_class, controller_class)

    # in Python 3.7 and above, it is guaranteed that the
    # order of iteration over a dictionary is similar to the order of insertion
    def build_components(self, components_desc: list[dict]):
        for comp in components_desc:
            self.create_component(comp['name'], comp['view'], comp['controller'])

    # in Python 3.7 and above, it is guaranteed that the
    # order of iteration over a dictionary is similar to the order of insertion
    def render(self):
        for id, comp in self._components.items():
            comp.get_view().render()

