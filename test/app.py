from streamsuperlit.model import SSTModel, Model
from streamsuperlit.controller import Controller
from streamsuperlit.view import View
import datetime
import streamlit as st

class MainPageController(Controller):

    def handle_button_click(self, *args, **kwargs):
        st.write(f'button clicked - {datetime.datetime.now()}')
        self._view.a += 1

class MainPageView(View):
    def __new__(cls, id: str, controller: 'streamsuperlit.controller.Controller'):
        return super(MainPageView, cls).__new__(cls, id, controller)

    def __init__(self, id: str, controller: MainPageController):
        st.write(f'view init {datetime.datetime.now()}')
        self.a = 10
        super().__init__(id, controller)
 
    def _view(self):
        st.title('Test page')
        st.write('MainPageView')
        st.button('click me', on_click=self._ctrl.handle_button_click)
        st.button('click me 2')
        st.write(self.a)

st.write(f'here - {datetime.datetime.now()}')
sst = SSTModel()
ctrl = MainPageController('main-page-ctrl-id', sst)
view = MainPageView('main-page-view-id', ctrl)
sst.register_controller(ctrl)
sst.register_view(view)
view.render()