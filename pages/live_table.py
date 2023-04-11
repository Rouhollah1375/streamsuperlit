import streamlit as st
import pandas as pd
import numpy as np
import toml
import mysql.connector
from streamlit_autorefresh import st_autorefresh
from datetime import datetime as dt
import threading
import sys


st.set_page_config(layout="wide")
st_autorefresh(interval=1 * 10 * 1000, key="dataframerefresh")

if 'filter_mode' not in st.session_state:
    st.session_state['filter_mode'] = False

def load_data():
    toml_data = toml.load("./configs/secrets.toml")
    # saving each credential into a variable
    HOST_NAME = toml_data['mysql']['host']
    DATABASE = toml_data['mysql']['database']
    PASSWORD = toml_data['mysql']['password']
    USER = toml_data['mysql']['user']
    PORT = toml_data['mysql']['port']

    mydb = mysql.connector.connect(host=HOST_NAME, database=DATABASE, user=USER, passwd=PASSWORD, use_pure=True, port=PORT)
    
    df = pd.read_sql('SELECT * FROM crawler_divar_post_info ORDER BY crawl_timestamp DESC LIMIT 300;' , mydb)

    return preprocess_data(df)

def preprocess_data(df: pd.DataFrame):
    df_ = df.copy()
    df_['subtitle_neighborhood'] = df_['subtitle_neighborhood'].str.strip()
    return df_

df = load_data()

def apply_filter_df(df: pd.DataFrame):
    filtered_df = df
    if is_agency == 'agency': 
        filtered_df = filtered_df[filtered_df['is_agency_pred'] == 1]
    if is_agency == 'personal': 
        filtered_df = filtered_df[filtered_df['is_agency_pred'] == 0]
    if parking_filter:
        filtered_df = filtered_df[filtered_df['parking'] == parking_filter]
    if elevator_filter:
        filtered_df = filtered_df[filtered_df['elevator'] == elevator_filter]    
    if storeroom_filter:
        filtered_df = filtered_df[filtered_df['storeroom'] == storeroom_filter]        
    if neighborhood_filter:
        filtered_df = filtered_df[filtered_df['subtitle_neighborhood'].isin(neighborhood_filter)]
    if agency_filter:
        filtered_df = filtered_df[filtered_df['agency_name'].isin(agency_filter)]

    
    filtered_df = filtered_df[(filtered_df['crawl_timestamp'].dt.date >= date_filter[0]) & \
                                (filtered_df['crawl_timestamp'].dt.date <= date_filter[1])]
    filtered_df = filtered_df[(filtered_df['total_price'] < price_filter[1]) & (filtered_df['total_price'] > price_filter[0])]  
    filtered_df = filtered_df[(filtered_df['house_area'] < area_filter[1]) & (filtered_df['house_area'] > area_filter[0])]
    
    return filtered_df
    
def color_coding(row):
    return ['background-color:#1f5c7a'] * len(row) if row.is_shakhsi > 0.8 else ['background-color:#303030'] * len(row)

st.title('Divar crawler dashboard')

st.checkbox("Use container width", value=False, key="use_container_width")

date_filter = st.sidebar.date_input('Crawl date: ', value = (dt(dt.today().year, dt.today().month, dt.today().day), dt(dt.today().year, dt.today().month, dt.today().day )))

neighborhoods = list(df['subtitle_neighborhood'].unique())
neighborhood_filter = st.sidebar.multiselect('Neighborhood:', neighborhoods)

st.sidebar.markdown("<h3 style='text-align: center; color: lightred; margin-bottom:-50px; margin-top:20px'> Ad provider </h3>", unsafe_allow_html=True)
is_agency = st.sidebar.radio(' ', ['personal', 'agency', 'both'])

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

run_btn = st.sidebar.button('Filter', key='e')
if run_btn:
    st.session_state['filter_mode'] = not st.session_state['filter_mode']
    print('hello', st.session_state['filter_mode'])

if st.session_state['filter_mode']:
    st.dataframe(apply_filter_df(df).style.apply(color_coding, axis=1))
else:
    st.dataframe(df.style.apply(color_coding, axis=1))


st.markdown(
    f'<h3 style="text-align: center;">Total length of the DataFrame: {len(df)}</h3>',
    unsafe_allow_html=True
)

max_price_index = df[df['total_price'] == df['total_price'].max()].index[0]
st.markdown(f"The most expensive house is located at: {df.loc[max_price_index, 'subtitle_neighborhood']}  \n with total price of: { '{:,}'.format(int(df.loc[max_price_index, 'total_price']))}")

min_price_index = df[df['total_price'] == df['total_price'].min()].index[0]
st.write(f"The cheapest house is located at: { df.loc[min_price_index, 'subtitle_neighborhood']}  \n with total price of: { '{:,}'.format(int(df.loc[min_price_index, 'total_price']))}")

max_area_index = df[df['house_area'] == df['house_area'].max()].index[0]
st.write(f"The area of the largest house is: { df.loc[max_area_index, 'house_area']}  \n located at: { df.loc[max_area_index, 'subtitle_neighborhood']}")

min_area_index = df[df['house_area'] == df['house_area'].min()].index[0]
st.write(f"The area of the smallest house is: { df.loc[min_area_index, 'house_area']}  \n located at: { df.loc[min_area_index, 'subtitle_neighborhood']}")