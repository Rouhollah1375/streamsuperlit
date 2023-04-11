import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime as dt
from datetime import timedelta
from controllers import LiveTablePageController, FilterStatus

st.set_page_config(layout="wide")
st_autorefresh(interval=1 * 10 * 1000, key="dataframerefresh")
if 'live-table-page-controller' not in st.session_state:
    st.session_state['live-table-page-controller'] = LiveTablePageController()

ctrl: LiveTablePageController = st.session_state['live-table-page-controller']
df = ctrl.get_df()

print('ctrl created at', ctrl.creation_time)

st.title('Divar crawler dashboard')

st.checkbox("Use container width", value=False, key="use_container_width")

date_filter = st.sidebar.date_input('Crawl date: ', 
                                    value=(dt.now()-timedelta(weeks=1), dt.now()))

neighborhoods = list(df['subtitle_neighborhood'].unique())
neighborhood_filter = st.sidebar.multiselect('Neighborhood:', neighborhoods)

st.sidebar.markdown("<h3 style='text-align: center; color: lightred; margin-bottom:-50px; margin-top:20px'> Ad provider </h3>", unsafe_allow_html=True)
is_agency = st.sidebar.radio(' ', ['personal', 'agency', 'both'])
agency_filter = []
agencies = list(df['agency_name'].unique())
if is_agency != 'personal':
    agency_filter = st.sidebar.multiselect('Select agency: ', agencies)

st.sidebar.markdown("<h3 style='text-align: center; color: lightred; margin-bottom:-75px; margin-top:20px;'> Area range </h3>", unsafe_allow_html=True)
area_filter = st.sidebar.slider('Area', min_value=int(df['house_area'].min())-1, max_value=int(df['house_area'].max())+1 , step=1, value=[int(df['house_area'].min())-1, int(df['house_area'].max())+1], label_visibility='hidden')

st.sidebar.markdown("<h3 style='text-align: center; color: lightred; margin-bottom: -15px; margin-top:20px;'> Price range </h3>", unsafe_allow_html=True)
price_filter = st.sidebar.slider('Price', min_value=int(df['total_price'].min())-1, max_value=int(df['total_price'].max())+1 , step=100000000, value=[int(df['total_price'].min())-1, int(df['total_price'].max())+1], label_visibility='collapsed')

st.sidebar.markdown("<h3 style='text-align: center; color: lightred; margin-bottom:-10px; margin-top:30px;'> More options </h3>", unsafe_allow_html=True)

parking_filter = st.sidebar.checkbox('Parking availability', value=False)
placeholder = st.empty()


elevator_filter = st.sidebar.checkbox('Elevator availability', value=False)
placeholder = st.empty()

storeroom_filter = st.sidebar.checkbox('Storeroom availability', value=False)
placeholder = st.empty()

filter_button = st.sidebar.button('Filter',
                                  key='e',
                                  on_click=ctrl.toggle_filter_button)

def display_main_table():
    filter = FilterStatus()
    filter.agency_names = agency_filter
    filter.neighborhoods = neighborhood_filter
    filter.parking = parking_filter
    filter.elevator = elevator_filter
    filter.storeroom = storeroom_filter
    filter.from_dt, filter.to_dt = date_filter
    filter.from_area, filter.to_area = area_filter
    filter.from_price, filter.to_price = price_filter

    df_to_display = ctrl.handle_apply_filter(filter)
    st.dataframe(df_to_display)

display_main_table()