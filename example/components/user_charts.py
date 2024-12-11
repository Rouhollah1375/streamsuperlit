from streamsuperlit import View, Controller, Component
from streamsuperlit.lifecycle_hook import OnInit
from streamsuperlit.lifecycle_hook import AfterInit
from uuid import uuid4

import streamlit as st
from streamlit_autorefresh import st_autorefresh
import numpy as np

class DailyUsersChartController(Controller, OnInit):
    def on_init(self):
        self.set_users_data()

    def _generate_numbers(self):
        return np.random.randint(10000, 15000, size=100)

    def set_users_data(self):
        self.data = self._generate_numbers()


class MonthlyUsersChartController(Controller, OnInit):
    def on_init(self):
        self.set_users_data()

    def _generate_numbers(self):
        return np.convolve(np.random.randint(100000, 150000, size=50), 1/5*np.ones(5), mode='valid')

    def set_users_data(self):
        self.data = self._generate_numbers()


class UsersChartView(View, AfterInit):
    def __new__(cls, id: str):
        return super(UsersChartView, cls).__new__(cls, id)

    def __init__(self, id: str):
        super().__init__(id)
        
    def _view(self):
        st.line_chart(self._ctrl.data)
        st.button('Fetch Data', on_click=self._ctrl.set_users_data,
                  key=uuid4().hex)

daily_users_chart_component = Component(name='daily-users-chart', id='id-1236',
          view_cls=UsersChartView,
          controller_cls=DailyUsersChartController)

monthly_users_chart_component = Component(name='monthly-users-chart', id='id-1237',
          view_cls=UsersChartView,
          controller_cls=MonthlyUsersChartController)