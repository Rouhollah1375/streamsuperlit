import streamlit as st
import pandas as pd

# @st.cache
def price_per_neighborhood(post_info_df: pd.DataFrame):
    a = post_info_df.groupby(by='neighborhood').agg({
        'total_price': 'mean',
        'today_total_price': 'mean',
        'post_id': 'count'
    }).rename(columns={'total_price': 'میانگین قیمت کل ملک', 'today_total_price': 'میانگین قیمت کل بروزشده', 'post_id': 'تعداد پست‌ها'})

    b = post_info_df.groupby(by='neighborhood').agg({
        'house_area': 'sum',
        'today_total_price': 'sum',
        'total_price': 'sum'
    })
    b['میانگین قیمت متری بروزشده'] = b['today_total_price'] / b['house_area']
    b['میانگین قیمت متری'] = b['total_price'] / b['house_area']
    b = b.drop(columns=['house_area', 'today_total_price', 'total_price'])


    res = pd.merge(b, a, on='neighborhood')
    return res

def filter_ppn(ppn_df: pd.DataFrame, column: str, low: float, high: float):
    return ppn_df.loc[ppn_df[column].between(low, high)]