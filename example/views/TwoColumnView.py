from streamsuperlit.view import View
import streamlit as st

class TwoColumnView(View):
    import pandas as pd
    def __new__(cls, id: str):
        return super(TwoColumnView, cls).__new__(cls, id)

    def __init__(self, id: str):
        self.df = self.pd.DataFrame({
            'id': ['assddf', 'wer', 'sdfxcv', 'rghgh', 'ertertccv'],
            'balance': [1, -2, 12, 99, 54],
            'name': ['ali', 'mammad', 'zahra', 'taghi', 'zak']
        })
        super().__init__(id)

    def _view(self):
        st.text('**small-component**\nThis component has two columns')
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(self.df)
        with col2:
            st.line_chart(self.df.balance)