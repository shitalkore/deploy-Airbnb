import streamlit as st
import time
from predict import show_predict_page
from explore_page_2 import show_explore_page
import os
import pickle
from pipeline import *
import re
from page import load_city

from stats import show_statistics


st.set_page_config(page_title='AirBnB')

city_re = re.compile('DataInterface_(.*)\.obj')
city_list = [city_re.findall(file)[0] for file in os.listdir('.') if city_re.match(file)]

with st.spinner('Loading...'):
    time.sleep(0.1)


city=st.sidebar.selectbox('Select City :',city_list)
city=city if city is not None else 'denver'

@st.cache
def get_data_interface(city):
    return pickle.load(open(f'DataInterface_{city}.obj','rb'))

data_interface=get_data_interface(city)


def get_revenue_model():
    return data_interface.get_model('revenue')

def get_booking_rate_model():
    return data_interface.get_model('booking_rate')


def get_insight():
    return data_interface.get_insight_engine()


page = st.sidebar.radio('Explore Data Or Predict', ("Predict", "Explore Data","Statistics","load"),horizontal =True)

if page == "Predict":
    show_predict_page( get_revenue_model(),get_booking_rate_model(),get_insight().describe)
    
elif page == 'Statistics':
    show_statistics(get_insight().describe)  
elif page == 'load':
    load_city()
else:
    show_explore_page(get_insight().insights)
    



    



