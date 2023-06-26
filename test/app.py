from streamsuperlit.model import SSTCore, Model
from streamsuperlit.controller import Controller
from streamsuperlit.view import View
import datetime
import streamlit as st

class MainPageController(Controller):

    def handle_button_click(self):
        st.write(f'button clicked - {datetime.datetime.now()}')
        self._view.a += 1
        self._view.b = 'even' if self._view.a % 2 == 0 else 'odd'
    
    def is_email(self):
        email = st.session_state[self._view._id+'3']
        self._view.is_email = '@' in email

class MainPageView(View):
    def __new__(cls, id: str):
        return super(MainPageView, cls).__new__(cls, id)

    def __init__(self, id: str):
        st.write(f'view init {datetime.datetime.now()}')
        self.a = 10
        self.b = None
        self.is_email = None

        super().__init__(id)
 
    def _view(self):
        st.title('Test page')
        st.write('MainPageView')
        st.button('click me', on_click=self._ctrl.handle_button_click, key=self._id+'1')
        st.button('click me 2', key=self._id+'2')
        st.text_input('email:', on_change=self._ctrl.is_email, key=self._id+'3')
        st.write(self.a)
        st.write(self.b)
        if self.is_email:
            st.write('email is correct')
        else:
            st.write('email is wrong')

components = [
    {
        'name': 'c1',
        'view': '__main__.MainPageView',
        'controller': '__main__.MainPageController'
    },
    {
        'name': 'c2',
        'view': '__main__.MainPageView',
        'controller': '__main__.MainPageController'
    }
]

sst = SSTCore(components)
sst.render()
