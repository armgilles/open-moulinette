# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 12:45:22 2015

Pour lire un fichier: on a besoin de plusieurs éléments: 
    - le nom que l'on va utiliser dans le code
    - l'url sur lequel on peut télécharger le zip
    - le nom du que l'on veut utiliser pour le fichier excel
"""

import os
import pandas as pd
from get_data import (read_equipement_file, change_headers,
                      sum_of_all_features,
                      revenu_url, _read_file_or_download, 
                      path_data)




##### équipements  #####

equipements = dict(
    commerce = ('equip-serv-commerce', None),
    sport = ('equip-sport-loisir-socio',
                      ['NB_F101', 'NB_F102', 'NB_F103', 'NB_F104',
                     'NB_F105', 'NB_F106', 'NB_F107', 'NB_F108',
                     'NB_F109', 'NB_F110', 'NB_F111', 'NB_F112',
                     'NB_F113', 'NB_F114', 'NB_F115', 'NB_F117', 'NB_F118']),
    enseignement_degre_1 = ('equip-serv-ens-1er-degre', ['NB_C101', 'NB_C102', 'NB_C104', 'NB_C105']),
    enseignement_degre_2 = ('equip-serv-ens-2eme-degre', ['NB_C201', 'NB_C301', 'NB_C302', 'NB_C303',
                              'NB_C304', 'NB_C305']),
    enseignement_sup = ('equip-serv-ens-sup-form-serv',
                                ['NB_C401', 'NB_C402', 'NB_C403',
                                'NB_C409', 'NB_C501', 'NB_C502',
                                'NB_C503', 'NB_C504', 'NB_C509',
                                'NB_C601', 'NB_C602', 'NB_C603',
                                'NB_C604', 'NB_C605', 'NB_C609',
                                'NB_C701', 'NB_C702']),
     social = ('equip-serv-action-sociale', None),
     sante = ('equip-serv-sante', None),
     medical = ('equip-serv-medical-para', None),
     service_particulier = ('equip-serv-particuliers', None),
     transport_tourisme = ('equip-tour-transp', None),
     )

def routine1(name):
    assert name in equipements
    filename, list_to_sum = equipements[name]
    df = read_equipement_file(filename)
    df = change_headers(df, headers_line=4)
    df = sum_of_all_features(df, 'nb_' + name, list_to_sum)
    assert len(df) == df.CODGEO.nunique()
    return df
    
equip_data = None
for table in equipements:
    print('* lecture de ' + table)
    if equip_data is None:
        equip_data = routine1(table)
    else:
        equip_data = equip_data.merge(routine1(table), how='outer')


##### revenus  #####

table_revenu = ['RFST', 'RFDM', 'RFDP', 'RFDU'] # l'ordre n'est pas 
# aléatoire, c'est celui du fichier zip (ordre alphabétique) de 2011
useless_cols = ['IRIS','LIBIRIS','COM','LIBCOM','REG','DEP','ARR','CV','ZE2010']

def routine2(year):
    url_path = revenu_url(year)
    names = [x + str(year) + 'IRI.xls' for x in table_revenu]
    _read_file_or_download(names, path_data, url_path)
    data = None
    for name in names:
        path_file_on_disk = path_data + name
        df = pd.read_excel(path_file_on_disk, sheetname=1, header=6)
        assert all([x in df.columns for x in useless_cols])
        assert len(df) == df.IRIS.nunique()
        print("\t il y a ", len(df),
          " iris différentes pour et ",
          len(df.columns) - len(useless_cols), " features")
        if data is None:
            data = df
        else:
            data = data.merge(df, how='outer')
            assert len(data) == len(df)
    return data.rename(columns={'IRIS':'CODGEO'})

revenu = routine2(2011)

data = equip_data.merge(revenu, how='outer')

## petit bout de code pour voir ce qui s'ajoute
#cond = equip_data.CODGEO.isin(revenu.CODGEO)
#equip_data[cond]
#cond = revenu.CODGEO.isin(equip_data.CODGEO)
#revenu[~cond]


############################################################
####                CENSUS FILES
############################################################

## Logement
logement = pd.read_excel(path_data+'base-ic-logement-2011.xls', sheetname='IRIS')
# creating header from file
header = logement.loc[4].tolist()
logement.columns = header
logement.rename(columns={'IRIS':'CODGEO', 'LIBIRIS': 'LIBGEO'}, inplace=True)
# to get real values
logement = logement[5:]

# Adding CODGEO (iris ID) and other geo features witch are not in data
features = [x for x in header if x not in ['IRIS', 'LIBIRIS']]
[features.append(i) for i in ['CODGEO', 'LIBGEO']]

key = ['CODGEO', 'LIBGEO', 'COM', 'LIBCOM', 'REG', 'DEP', 'UU2010']

data = pd.merge(data, logement[features], on=key, how='outer')


## Diplome
diplome = pd.read_excel(path_data+'base-ic-diplomes-formation-2011.xls', sheetname='IRIS')
# creating header from file
header = diplome.loc[4].tolist()
diplome.columns = header
diplome.rename(columns={'IRIS':'CODGEO', 'LIBIRIS': 'LIBGEO'}, inplace=True)
# to get real values
diplome = diplome[5:]

# Adding CODGEO (iris ID) and other geo features witch are not in data
features = [x for x in header if x not in ['IRIS', 'LIBIRIS']]
[features.append(i) for i in ['CODGEO', 'LIBGEO']]

key = ['CODGEO', 'LIBGEO', 'COM', 'LIBCOM', 'REG', 'DEP', 'UU2010',
       'TRIRIS', 'GRD_QUART', 'TYP_IRIS', 'MODIF_IRIS', 'LAB_IRIS'] # This line has been load with Logement file

data = pd.merge(data, diplome[features], on=key, how='outer')


## Famille
famille = pd.read_excel(path_data+'base-ic-couples-familles-menages-2011.xls', sheetname='IRIS')
# creating header from file
header = famille.loc[4].tolist()
famille.columns = header
famille.rename(columns={'IRIS':'CODGEO', 'LIBIRIS': 'LIBGEO'}, inplace=True)
# to get real values
famille = famille[5:]

# Adding CODGEO (iris ID) and other geo features witch are not in data
features = [x for x in header if x not in ['IRIS', 'LIBIRIS']]
[features.append(i) for i in ['CODGEO', 'LIBGEO']]

key = ['CODGEO', 'LIBGEO', 'COM', 'LIBCOM', 'REG', 'DEP', 'UU2010',
       'TRIRIS', 'GRD_QUART', 'TYP_IRIS', 'MODIF_IRIS', 'LAB_IRIS'] # This line has been load with Logement file


data = pd.merge(data, famille[features], on=key, how='outer')


## Population
population = pd.read_excel(path_data+'base-ic-evol-struct-pop-2011.xls', sheetname='IRIS')
# creating header from file
header = population.loc[4].tolist()
population.columns = header
population.rename(columns={'IRIS':'CODGEO', 'LIBIRIS': 'LIBGEO'}, inplace=True)
# to get real values
population = population[5:]

# Adding CODGEO (iris ID) and other geo features witch are not in data
features = [x for x in header if x not in ['IRIS', 'LIBIRIS']]
[features.append(i) for i in ['CODGEO', 'LIBGEO']]

key = ['CODGEO', 'LIBGEO', 'COM', 'LIBCOM', 'REG', 'DEP', 'UU2010',
       'TRIRIS', 'GRD_QUART', 'TYP_IRIS', 'MODIF_IRIS', 'LAB_IRIS'] # This line has been load with Logement file

data = pd.merge(data, population[features], on=key, how='outer')


## Activité
activite = pd.read_excel(path_data+'base-ic-activite-residents-2011.xls', sheetname='IRIS')
# creating header from file
header = activite.loc[4].tolist()
activite.columns = header
activite.rename(columns={'IRIS':'CODGEO', 'LIBIRIS': 'LIBGEO'}, inplace=True)
# to get real values
activite = activite[5:]

# Adding CODGEO (iris ID) and other geo features witch are not in data
features = [x for x in header if x not in ['IRIS', 'LIBIRIS']]
[features.append(i) for i in ['CODGEO', 'LIBGEO']]

key = ['CODGEO', 'LIBGEO', 'COM', 'LIBCOM', 'REG', 'DEP', 'UU2010',
       'TRIRIS', 'GRD_QUART', 'TYP_IRIS', 'MODIF_IRIS', 'LAB_IRIS'] # This line has been load with Logement file

data = pd.merge(data, activite[features], on=key, how='outer')
