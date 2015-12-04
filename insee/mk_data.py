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
                      revenu_url, recensement_url, _read_file_or_download,
                      path_data)


##### équipements  #####



##### revenus  #####

table_revenu = ['RFST', 'RFDM', 'RFDP', 'RFDU'] # l'ordre n'est pas
# aléatoire, c'est celui du fichier zip (ordre alphabétique) de 2011
useless_cols = ['IRIS','LIBIRIS','COM','LIBCOM','REG','DEP','ARR','CV','ZE2010']

def info_revenus(year):
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



############################################################
####                CENSUS FILES
############################################################



population = info_population(2011)
