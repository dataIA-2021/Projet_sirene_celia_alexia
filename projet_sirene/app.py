#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 10 17:23:45 2022

@author: celiamato
"""

import streamlit as st
from multiapp import MultiApp
from apps import app0, app1, app2, app4 # import your app modules here
#from streamlit_option_menu import option_menu


app = MultiApp()
st.markdown("<h1 style='text-align: center; color: grey;'>Watercolor work areas</h1>", unsafe_allow_html=True)
st.write(' ')
st.write(' ')
st.write(' ')


#nav = st.sidebar.radio("Navigation",["Home","primaire","secondaire","tertiaire"])

# Add all your application here
#if nav == "Home":
#app.add_app("Home", app0.app)
#if nav == "primaire":
app.add_app("Primaire", app1.app)
#if nav == "secondaire":
app.add_app("Secondaire", app2.app)
#if nav == "tertiaire":
app.add_app("Tertiaire",app4.app)
    
    
# The main app
app.run()

