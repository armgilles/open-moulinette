# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 09:40:36 2015

@author: User
"""
import pandas as pd
from globals import path_insee, path_data, _read_file_or_download

def equipement_url(filename):
    url_path = path_insee + filename + '/' + filename + '-infra-13.zip'
    return url_path


def read_equipement_file(filename):
    url_path = equipement_url(filename)
    path_file_on_disk = path_data + filename + '-infra.xls'
    _read_file_or_download(filename + '-infra.xls', path_data, url_path)
    return pd.read_excel(path_file_on_disk, sheetname='IRIS', header=5)



def change_headers(iris_df, headers_line):
    ''' iris_df is an iris data frame'''
#    iris_df.rename(columns={'IRIS':'CODGEO'}, inplace=True)
    # to get real values
    iris_df = iris_df[5:]
    # clean Nan Columns
    iris_df.dropna(how='any', axis=1, inplace=True)
    return iris_df


def sum_of_all_features(iris_df, colname, list_to_sum=None):
    ''' iris_df is an iris data frame
        colname is the name of the sum of columns'''
    header = [x for x in iris_df.columns if str(x) != 'nan'] # remove NaN to header to create new sum feature
    # creating new feature : sum of all feature
    if list_to_sum is None:
        features = [x for x in header if x not in columns_not_to_sum]
    else:
        features = list_to_sum
    iris_df[colname] = iris_df[features].applymap(lambda x: float(x)).sum(axis=1)
    nb_features = len(features)
    print("\t il y a ", iris_df.CODGEO.nunique(),
          " iris différentes pour et ", nb_features, " features")
    return iris_df


key = ['CODGEO', 'LIBGEO', 'COM', 'LIBCOM', 'REG', 'DEP', 'UU2010']

columns_not_to_sum = ['CODGEO', 'LIBGEO', 'COM', 'LIBCOM', 'REG', 'DEP', 'ARR', 'CV',
             'ZE2010', 'UU2010', 'UU12010', 'ID_MODIF_GEO']

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

def info_equipement():
    equipement = None
    for table in equipements:
        print('* lecture de ' + table)
        if equipement is None:
            equipement = routine1(table)
        else:
            equipement = equipement.merge(routine1(table), how='outer')
    return equipement