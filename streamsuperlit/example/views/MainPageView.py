from streamsuperlit.view import View
import streamlit as st

class MainPageView(View):
    def __new__(cls, id: str):
        return super(MainPageView, cls).__new__(cls, id)

    def __init__(self, id: str):
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