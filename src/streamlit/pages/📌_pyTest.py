import streamlit.components.v1 as components
import streamlit as st
import streamlit_authenticator as stauth
from datetime import datetime
import yaml
import pandas as pd
import numpy as np
import time
import base64
from PIL import Image
import os
import requests
#import pymysql


with open('./streamlit_config.yaml') as file:
    config = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)


if st.session_state["authentication_status"]:
    HtmlFile = open("./pages/report.html", 'r')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 2000)
    
    
elif st.session_state["authentication_status"] == False:
    st.error('Username or Password is incorrect')
    st.session_state.token = ''
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')
    st.session_state.token = ''
    
with st.sidebar:
    if(st.session_state.authentication_status == True):
        st.info('User: ***%s***' % st.session_state.username)

        authenticator.logout('Logout')





    