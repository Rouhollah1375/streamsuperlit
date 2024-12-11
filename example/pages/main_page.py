from streamsuperlit import Component, View, Controller
from components.user_charts import daily_users_chart_component, monthly_users_chart_component 
from components.auto_refresh_component import auto_refresh_component
from streamlit_autorefresh import st_autorefresh
import streamlit as st

class MainPageView(View):
    def __new__(cls, id: str):
        return super(MainPageView, cls).__new__(cls, id)
    
    def __init__(self, id: str):
        super().__init__(id)

    def _view(self):
        st.text('component 1 view is here!')
        st.text(f'Message from the controller: {self._ctrl.get_message()}')

class MainPageController(Controller):
    def get_message(self) -> str:
        return 'Hello my view!!'


st_autorefresh(interval= 2 * 1000, key="id-autorefresh")

st.header('SST Components are created in the good old `View`-`Controller` style')
Component(name='main-page', id='id-1234', 
            view_cls=MainPageView,
            controller_cls=MainPageController)()

st.divider()

st.header('SST Components can be nested and reused!')
col1, col2 = st.columns(2)
with col1:
    st.subheader('Daily Users')
    daily_users_chart_component()
with col2:
    st.subheader('Monthly Users')
    monthly_users_chart_component()
 
st.header('Forget about `st.cache`. SST Components are persisted among page refreshes, button clicks, etc.')
auto_refresh_component()