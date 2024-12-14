from streamsuperlit import View, Controller, Component
from streamsuperlit.lifecycle_hook import OnInit
from streamsuperlit.lifecycle_hook import AfterInit

import streamlit as st
from streamlit_autorefresh import st_autorefresh
import datetime

class AutoRefreshController(Controller, OnInit):
    def on_init(self):
        self.a = 0

    def increment(self):
        print('hello')
        self.a += 1

    def get_a(self):
        return self.a

class AutoRefreshView(View, AfterInit):

    def _view(self):
        st.header('Auto Refresh Page')
        st.text(datetime.datetime.now())
        col1, col2 = st.columns(2, gap='small')
        with col1:
            st.text('See how this component\'s state is preserved across autorefreshes.\nIt never resets to 0, and only reacts to the button click:')
        with col2:
            st.button('click me', on_click=self._ctrl.increment)
            st.text(self._ctrl.a)
        st.json(st.session_state)

auto_refresh_component = Component(name='auto-refresh', id='id-1235',
          view_cls=AutoRefreshView,
          controller_cls=AutoRefreshController)