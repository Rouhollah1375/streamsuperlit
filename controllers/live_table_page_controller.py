import streamlit as st
import pandas as pd
import data_analysis.data_processing as dp
from datetime import datetime
from enum import Enum
import numpy as np

class PostProviderEnum(Enum):
    both = 0
    personal = 1
    agency = 2


class FilterStatus:
    post_provider = PostProviderEnum.agency
    parking = False
    elevator = False
    storeroom = False
    balcony = False
    neighborhoods: list[str] = []
    agency_names: list[str] = []
    from_dt = datetime(1970, 1, 1)
    to_dt = datetime(5000, 1, 1)
    from_price: float = -np.inf
    to_price: float = np.inf
    from_area: float = 0
    to_area: float = np.inf


class LiveTablePageController:
    def __init__(self):
        if 'filter_mode' not in st.session_state:
            st.session_state['filter_mode'] = False
        st.session_state['df'] = dp.load_data()
        self.creation_time = datetime.now()

    def update_data(self):
        st.session_state['df'] = dp.load_data()

    def get_df(self):
        return st.session_state['df']

    def apply_filter_df(self, filter: FilterStatus):
        filtered_df = self.get_df()
        if filter.post_provider == PostProviderEnum.agency: 
            filtered_df = filtered_df[filtered_df['tag'] == 'agency']
            print('agency')
        if filter.post_provider == PostProviderEnum.personal: 
            filtered_df = filtered_df[filtered_df['tag'] == 'personal']
            print('personal')
        if filter.parking:
            filtered_df = filtered_df[filtered_df['parking'] == filter.parking]
        if filter.elevator:
            filtered_df = filtered_df[filtered_df['elevator'] == filter.elevator]
        if filter.storeroom:
            filtered_df = filtered_df[filtered_df['storeroom'] == filter.storeroom]
        if filter.balcony:
            filtered_df = filtered_df[filtered_df['balcony'] == filter.balcony]

        if filter.neighborhoods:
            filtered_df = filtered_df[filtered_df['subtitle_neighborhood'].isin(filter.neighborhoods)]
        if filter.agency_names:
            filtered_df = filtered_df[filtered_df['agency_name'].isin(filter.agency_names)]

        
        filtered_df = filtered_df[(filtered_df['crawl_timestamp'].dt.date >= filter.from_dt) & \
                                    (filtered_df['crawl_timestamp'].dt.date <= filter.to_dt)]
        filtered_df = filtered_df[(filtered_df['total_price']*(10**-9) <= filter.to_price) & (filtered_df['total_price']*(10**-9) >= filter.from_price)]  
        filtered_df = filtered_df[(filtered_df['house_area'] <= filter.to_area) & (filtered_df['house_area'] >= filter.from_area)]
        
        return filtered_df

    def color_coding(self, row: pd.Series):
            return ['background-color:#1f5c7a'] * len(row) if row.is_shakhsi > 0.8 else ['background-color:#303030'] * len(row)
        
    def handle_apply_filter(self, filter: FilterStatus):
        if st.session_state['filter_mode']:
            print('filter on')
            return self.apply_filter_df(filter).style.apply(self.color_coding, axis=1)
        else:
            print('filter off')
            return self.get_df().style.apply(self.color_coding, axis=1)

    def toggle_filter_button(self):
        st.session_state['filter_mode'] = not st.session_state['filter_mode']

