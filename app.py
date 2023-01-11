import streamlit as st
import pandas as pd
import numpy as np
import jdatetime
from price_per_neighborhood import price_per_neighborhood, filter_ppn
import datetime

st.title('Divar Analysis Dashboard')

@st.cache
def load_data(file, from_date, to_date):
    if file == None:
        return None
    post_info_df = pd.read_csv(file)
    post_info_df['crawl_timestamp'] = pd.to_datetime(post_info_df['crawl_timestamp'])
    date_mask = (post_info_df['crawl_timestamp'].dt.date >= from_date) & (post_info_df['crawl_timestamp'].dt.date <= to_date)
    post_info_df = post_info_df.loc[date_mask]
    post_info_df['neighborhood'] = post_info_df['neighborhood'].str.strip()
    post_info_df = up_to_date_prices(post_info_df)
    return post_info_df

@st.cache
def up_to_date_prices(post_info_df):
    THIS_YEAR = jdatetime.date.today().year
    DECREASE_CAP_YEAR = 20
    YEARLY_DECREASE_RATE = 0.02

    def apply_rule(price, year_built):     
        if year_built < THIS_YEAR - DECREASE_CAP_YEAR:
            return price / (1 - DECREASE_CAP_YEAR * YEARLY_DECREASE_RATE)
        else:
            delta_year = THIS_YEAR - year_built
            return price / (1 - delta_year * YEARLY_DECREASE_RATE)
    
    post_info_df['today_total_price'] = post_info_df.apply(lambda row: apply_rule(row.total_price, row.year_built), axis=1)
    post_info_df['today_price_per_area'] = post_info_df.apply(lambda row: apply_rule(row.price_per_area, row.year_built), axis=1)

    return post_info_df

if __name__ == "__main__":
    with st.sidebar.container():
        st.sidebar.subheader('Dataset Properties')
        dataset_file = st.file_uploader('Upload a .csv file', accept_multiple_files=False, type=['csv'])
        col = st.sidebar.columns(2)
        from_date = col[0].date_input('From')
        to_date = col[1].date_input('To')

    post_info_df = load_data(dataset_file, from_date, to_date)

    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(post_info_df)
        st.write(f'Number of posts = {len(post_info_df)}')


    st.markdown('-------------')


    st.subheader('Price In Neighborhoods')

    ppn = price_per_neighborhood(post_info_df)
    with st.sidebar.container():
        st.sidebar.subheader('Price In Neighoborhood')
        ppn_price_range = st.sidebar.slider('Select a range (Million Tomans)', 0, 500, (30, 100))
        ppn_filter_column = st.sidebar.selectbox('column to apply range', ppn.columns)
        filtered_ppn = filter_ppn(ppn, ppn_filter_column, min(ppn_price_range)*1e6, max(ppn_price_range)*1e6)
        st.sidebar.markdown('------------')
    st.dataframe(filtered_ppn)