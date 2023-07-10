import streamlit as st
from streamsuperlit.model.sst_core import SSTCore
from streamsuperlit.component import Component

class Page:
    def __init__(self, name: str, components_list: list[dict]=None, components_json: str=None) -> None:
        self._name = name
        self._components = []

        if components_list is None and components_json is None:
            raise Exception('Either components or components_json must be provided when initializing page object.')
        if (not components_list is None) and (not components_json is None):
            raise Exception('Only one of components or components_json must be provided when initializing page object.')
        self._components_list = components_list
        self._components_json = components_json

        super().__init__()

    def __call__(self) -> None:
        self._components = SSTCore.get().render_page(
            self._name,
            components=self._components_list,
            components_json=self._components_json)