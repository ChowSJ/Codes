import streamlit as st

import pandas as pd
import numpy as np
import requests
import io
import re
import datetime

# Alpha vantage has restriction on total number of API that can be made ina  day. It is 25. The counter tracks number of 
# request

if "api_counter" not in st.session_state:
    st.session_state['api_counter']=0

def func_extract_info(function_call,symbol,api_key,datatype='csv'):
    url= 'https://www.alphavantage.co/query?function={}&symbol={}&datatype={}&apikey={}'.format(function_call,symbol,datatype,api_key)
    r=requests.get(url=url)
    data=io.StringIO(r.text)
    df=pd.read_csv(data)
    return df

with st.container(border=True):
    st.header(body='Stock UI Practice',divider=True)
    st.subheader(body="There is restriction of 25 requests. The number of requests in current session is: {}".format(st.session_state['api_counter']))


with st.container(border=True):
    col_chart,col_input=st.columns([0.7,0.3])

    with col_chart:
        placeholder_chart=st.empty()
        placeholder_chart.write('Space for Chart')
    with col_input:
        st.text_input(label='Please enter your API key',type='password',
                      help="Please enter API provideed by https://www.alphavantage.co/support/#api-key",placeholder='API KEY',key='api_key')
        st.text_input(label='Please enter your Stock of interest',help="Please enter code only.",placeholder='STOCK CODE',key='symbol')
        if st.session_state['symbol']:
            st.session_state['api_counter']+=1
            df_stock=func_extract_info(function_call='TIME_SERIES_DAILY',symbol=st.session_state['symbol'],api_key=st.session_state['api_key'])
            placeholder_chart.line_chart(data=df_stock,x='timestamp',y='close',use_container_width=True)
if st.session_state['api_counter']<1:
    st.empty()
else:
    with st.container(border=True):
        st.dataframe(df_stock,use_container_width=True)