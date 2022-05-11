#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 10 08:28:21 2022

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



conn.autocommit = True
cursor = conn.cursor()
print("Database opened successfully")

data = pd.read_sql('select * from allinone limit 1000', conn)


def app(): 

        st.markdown("<h2 style='text-align: center; color: black;'>Cartographie des secteurs d'activité français </h2>", unsafe_allow_html=True)
        st.write(' ')
        st.write(' ')
        st.write(' ')
        
        option = st.selectbox('Selection du secteur d''activité', data['intitule1'].unique())
        st.write('Vous avez sélectionné : ', option)

    
        map_element = folium.Map(location=[46.227638,2.213749], zoom_start=6, tiles='Stamen Watercolor')
        
        loc=data[['latitude','longitude']].loc[data.intitule1.str.contains(option)]
      
        folium.CircleMarker(loc ,radius=2, weight=1,
                                color='darkorange',
                                fill_opacity=0.9
                                # popup=
                                #       f'<b>Commune: </b>{str(data["nom_de_la_commune"])}'
                                #       f'<br></br>'f'<b>Code postal: </b>{str(data["code_postal"])}'
                                #       f'<br></br>'f'<b>Siren: </b>{str(data["siren"])}'
                                #       f'<br></br>'f'<b>Date de création: </b>{str(data["dateCreationEtablissement"])}'
        
                                ).add_to(map_element)
        
        
        folium.Marker(location=[47.394144, 0.68484],
                                    popup='Tours City',
                                    icon=folium.Icon(color='green', icon='ok-sign')
                                    ).add_to(map_element)
        
        
        folium_static(map_element)

        






