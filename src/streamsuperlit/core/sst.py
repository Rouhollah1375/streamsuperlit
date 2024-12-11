from streamsuperlit.view import View
from streamsuperlit.controller import Controller
from streamsuperlit.component import Component
from streamsuperlit.core.uuid import UUID
from streamsuperlit.core.utils import get_class
from collections import OrderedDict
import json
import streamlit as st

SSTCORE_ID = 'sst-core'         # TODO: Do not let any other object(view, components, etc. ) set this id for itself.

class SSTCore:
    def __new__(cls):
        if SSTCore.get() is None:
            st.session_state[SSTCORE_ID] = super(SSTCore, cls).__new__(cls)
            st.session_state['core-init'] = False
        return SSTCore.get()

    def __init__(self):
        if not st.session_state['core-init']:
            self._uuid = UUID()
            self._pages_components: dict[str, OrderedDict] = {}
            st.session_state['core-init'] = True

        super().__init__()
    
    @classmethod
    def get(cls):
        if SSTCORE_ID not in st.session_state:
            return None
        return st.session_state[SSTCORE_ID]

    def _create_component(self, name: str, view_cls: str, controller_cls: str):
        id = self._uuid.get_uuid()
        try:
            view_class = get_class(view_cls)
            controller_class = get_class(controller_cls)
        except:
            raise Exception(f'Cannot create the component {name}. view_cls or controller_cls are not properly provided.')
        return Component(name, id, view_class, controller_class), id

    def _build_components(self, components_desc: list[dict]):
        components = OrderedDict()
        for comp in components_desc:
            c, id = self._create_component(comp['name'], comp['view'], comp['controller'])
            components[id] = c
        return components

    def render_page(self, page_name: str, components: list[dict]=None, components_json: str=None):
        if components_json:
            with open(components_json, 'r') as f:
                components = json.load(f)
        if page_name in self._pages_components.keys():
            built_comps = self._pages_components[page_name]
        else:
            built_comps = self._build_components(components)
            self._pages_components[page_name] = built_comps
            
        for id, comp in self._pages_components[page_name].items():
            comp.get_view().render()

        return self._pages_components[page_name]

