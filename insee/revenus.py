# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 09:38:50 2015

"""
import pandas as pd
from globals import path_insee, path_data, _read_file_or_download


def revenu_url(year):
    filename = 'structure-distrib-revenus'
    general_url = path_insee + filename + '/'
    year_folder =  filename + '-' + str(year) + '/'
    zip_name = filename + '-iris-' + str(year) + '.zip'
    return general_url + year_folder + zip_name


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