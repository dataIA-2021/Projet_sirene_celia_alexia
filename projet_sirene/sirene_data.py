# -*- coding: utf-8 -*-
"""
Created on Thu May  5 14:08:06 2022

@author: Greta
"""

import pandas as pd
import yaml
import psycopg2
import csv
from sqlalchemy import create_engine
import os

col_use = ['siren', 'siret','dateCreationEtablissement', 
'numeroVoieEtablissement', 
'typeVoieEtablissement', 'libelleVoieEtablissement',
'codePostalEtablissement', 'libelleCommuneEtablissement', 'activitePrincipaleEtablissement',
]


data_ent = pd.read_csv(r'C:\Users\Greta\Desktop\projet_sirene\StockEtablissement_utf8\StockEtablissement_utf8.csv', usecols= col_use,  encoding='utf8')




#data_ent.to_csv('entreprises.csv', sep=";", index=True)

data_post= pd.read_csv(r'C:\Users\Greta\Desktop\projet_sirene\laposte_hexasmal.csv', sep=';')
data_post[['latitude','longitude']]=data_post.coordonnees_gps.str.split(',',expand=True)
data_post['latitude']= data_post.latitude.astype(float)
data_post['longitude']= data_post.longitude.astype(float)


data_naf= pd.read_excel(r'C:\Users\Greta\Desktop\projet_sirene\int_courts_naf_rev_2.xls')
data_naf_clean = data_naf.iloc[: , 1:]

data_naf_clean = data_naf_clean.dropna(subset=['Code'], how='all').drop_duplicates().reset_index()
data_naf_clean.drop_duplicates()

# Pour load le yaml fichiers avec paramètres : !!! Attention changer le chemin sur votre machine !!!
with open(r'C:\Users\Greta\Desktop\projet_sirene\config.yml','r') as f:
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


engine = create_engine('postgresql://mato:fc2c2fcd3d5f86b4b5775879149490566d68c34d92b4dd76041e6e300c2c20bc@localhost:5433/mato')
# data_ent.to_sql('entreprises', engine, chunksize=20, if_exists="replace")
#data_post.to_sql('coordonnees', engine,  if_exists="replace")
#data_naf_clean.to_sql('naf', engine,  if_exists="replace")

'''
SELECT nom_de_la_commune,code_postal,latitude,longitude , siren, "dateCreationEtablissement", 
"numeroVoieEtablissement","typeVoieEtablissement","libelleVoieEtablissement","codePostalEtablissement",
"libelleCommuneEtablissement","activitePrincipaleEtablissement","Code",intitule1
FROM public.entreprises
JOIN public.coordonnees ON (coordonnees."code_postal"= entreprises."codePostalEtablissement")
JOIN public.naf ON (entreprises."activitePrincipaleEtablissement" = naf."Code")
LIMIT 10;
'''