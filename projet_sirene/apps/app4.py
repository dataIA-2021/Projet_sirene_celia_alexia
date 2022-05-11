#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 10 21:14:23 2022

@author: celiamato
"""


import pandas as pd
import yaml
#import toml
import psycopg2
import csv
from sqlalchemy import create_engine, event
import os
import streamlit as st
import streamlit.components.v1 as components
from streamlit_folium import folium_static

#Import folium and related plugins
import folium 
from folium import Marker
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap
import urllib.parse
import random

import branca.colormap as cm
from collections import defaultdict
from sqlalchemy import inspect


#Pour load le yaml fichiers avec paramètres : !!! Attention changer le chemin sur votre machine !!!
with open(r'config.yml','r') as f:
    conf= yaml.safe_load(f)
my = conf['PG']

print(my)
    
# Connexion à la base de données postgresql
conn = psycopg2.connect(host=my['host'],
                user=my['user'],
                password =my['password'],
                port=my['port'],
                database=my['database'])



#conn.autocommit = True
cursor = conn.cursor()
print("Database opened successfully")


engine = create_engine('postgresql://mato:fc2c2fcd3d5f86b4b5775879149490566d68c34d92b4dd76041e6e300c2c20bc@localhost:5433/mato')




data_trans = pd.read_sql('select * from transport limit 1000', conn)

def app():
    
    col1, col2= st.columns(2)
    
    with col1:
            st.markdown("<h2 style='text-align: center; color: black;'>Densité des secteurs d'activité tertiaire </h2>", unsafe_allow_html=True)
    with col2:
            st.image("https://www.morbihan.cci.fr/sites/ccimorbihan/files/resize/commerce_bleu_sombre-200x200.png", width=160)
     
    st.write(' ')
    st.write(' ')
    st.write(' ')    
     
    option_trans= st.selectbox('Selection du secteur d''activité', data_trans['intitule1'].unique())
    st.write('Vous avez sélectionné : ', option_trans)    
    
    
        
    m = folium.Map([46.227638,2.213749], zoom_start=6, tiles = "Stamen Watercolor")
                       
    HeatMap(data_trans[['latitude','longitude']].loc[data_trans.intitule1.str.contains(option_trans)]).add_to(m)
    folium.Marker(
                            location=[47.394144, 0.68484],
                                popup='Tours City',
                                icon=folium.Icon(color='green', icon='ok-sign')).add_to(m)
    
 
    
    folium_static(m)
      