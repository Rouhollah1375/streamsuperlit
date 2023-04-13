import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime as dt
from datetime import timedelta
from controllers import LiveTablePageController, FilterStatus, PostProviderEnum

st.set_page_config(layout="wide")
st_autorefresh(interval= 5 * 1000, key="dataframerefresh")

if 'live-table-page-controller' not in st.session_state:
    st.session_state['live-table-page-controller'] = LiveTablePageController()

ctrl: LiveTablePageController = st.session_state['live-table-page-controller']
df = ctrl.get_df()

st.title('Divar crawler dashboard')

st.checkbox("Use container width", value=False, key="use_container_width")

if st.session_state['filter_mode']:
    st.markdown("<h1 style='text-align: center; color: ;  margin-top:20px'> Filters <span style=color:green> On! </span> </h3>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center; color: ; margin-top:20px'> Filters <span style=color:red> Off! </span> </h3>", unsafe_allow_html=True)

date_filter = st.sidebar.date_input('Crawl date: ', value=(dt.now()-timedelta(weeks=10), dt.now()))

neighborhoods = list(df['subtitle_neighborhood'].unique())
neighborhood_filter = st.sidebar.multiselect('Neighborhood:', neighborhoods)

st.sidebar.divider()

st.sidebar.markdown("<h3 style='text-align: center; color: #36a9e1; margin-bottom:-25px; margin-top:0px'> Post provider </h3>", unsafe_allow_html=True)
is_agency = st.sidebar.radio(' ', ['both','personal', 'agency'], index=0)
agency_filter = []
agencies = list(df['agency_name'].unique())
if is_agency == 'agency':
    agency_filter = st.sidebar.multiselect('Select agency: ', agencies)

st.sidebar.divider()

st.sidebar.markdown("<h3 style='text-align: center; color: #36a9e1; margin-bottom:-25px; margin-top:0px;'> Total area range(Meter) </h3>", unsafe_allow_html=True)
area_filter = st.sidebar.slider('Area', min_value=int(df['house_area'].min())-1, max_value=int(df['house_area'].max())+1 , step=1, value=[int(df['house_area'].min())-1, int(df['house_area'].max())+1], label_visibility='hidden')

st.sidebar.divider()

st.sidebar.markdown("<h3 style='text-align: center; color: #36a9e1; margin-bottom: 20px; margin-top:0px;'> Total price range(Billions) </h3>", unsafe_allow_html=True)
price_filter = st.sidebar.slider('Price', min_value=float(df['total_price'].min()*(10**-9)), max_value=float(df['total_price'].max()*(10**-9)) , step=0.01, value=[float(df['total_price'].min()*(10**-9)), float(df['total_price'].max()*(10**-9))], label_visibility='collapsed')
st.sidebar.write('From', price_filter[0], 'billions, to ', price_filter[1], 'billions')

st.sidebar.divider()

st.sidebar.markdown("<h3 style='text-align: center; color: #36a9e1; margin-bottom:20px; margin-top:0px;'> More options </h3>", unsafe_allow_html=True)

parking_filter = st.sidebar.checkbox('Parking availability', value=False)
placeholder = st.empty()

elevator_filter = st.sidebar.checkbox('Elevator availability', value=False)
placeholder = st.empty()

storeroom_filter = st.sidebar.checkbox('Storeroom availability', value=False)
placeholder = st.empty()

columns = st.sidebar.columns((2, 2, 2))
filter_button = columns[1].button('Filter',
                                  key='e',
                                  on_click=ctrl.toggle_filter_button)

def display_main_table():
    filter = FilterStatus()
    filter.agency_names = agency_filter
    filter.post_provider = PostProviderEnum[is_agency]
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
ctrl.update_data()