# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 12:45:22 2015
@author: Florian, Alexis
"""

import os
import pandas as pd
from get_data import download_unzip

path_insee = 'http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/'

##################### IMPORT DES DONNEES COMMUNES ############################

''' Import des données IRIS grâce à l'open-moulinette'''
print("Initialisation...")

path_data = 'data/'
assert os.path.exists(path_data), 'il faut créer le fichier correspondant à path data'


key = ['CODGEO', 'LIBGEO', 'COM', 'LIBCOM', 'REG', 'DEP', 'UU2010']

columns_not_to_sum = ['CODGEO', 'LIBGEO', 'COM', 'LIBCOM', 'REG', 'DEP', 'ARR', 'CV',
             'ZE2010', 'UU2010', 'UU12010', 'ID_MODIF_GEO']


def insee_path_by_filename(filename):
    url_path = path_insee + filename + '/' + filename + '-infra-13.zip'
    return url_path


def _read_iris_file(filename):
    path_file_on_disk = path_data + filename + '-infra.xls'
    if not os.path.exists(path_file_on_disk):
        url_path = insee_path_by_filename(filename)
        download_unzip(url_path, path_data)
    return pd.read_excel(path_file_on_disk, sheetname='IRIS')



def _change_headers(iris_df):
    ''' iris_df is an iris data frame'''
#    iris_df.rename(columns={'IRIS':'CODGEO'}, inplace=True)
    header = iris_df.loc[4].tolist()
    iris_df.columns = header
    # to get real values
    iris_df = iris_df[5:]
    # clean Nan Columns
    iris_df.dropna(how='any', axis=(1), inplace=True)
    return iris_df


def _sum_of_all_features(iris_df, colname, list_to_sum=None):
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
    print("\t il y a ", len(iris_df.CODGEO.unique()),
          " iris différentes pour et ", nb_features, " features")
    return iris_df


def routine1(name):
    assert name in iris_table
    filename, list_to_sum = iris_table[name]
    df = _read_iris_file(filename)
    df = _change_headers(df)
    df = _sum_of_all_features(df, 'nb_' + name, list_to_sum)

    return df

iris_table = dict(
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


data = None
for table in iris_table:
    print('* lecture de ' + table)
    if data is None:
        data = routine1(table)
    else:
        data = data.merge(routine1(table), how='outer')


### Revenu have 4 files [ménage, personne, unité de consomation, ensemble]
#-------------------------------------------------------------------------

## Revenu Ménage
revenu_menage = pd.read_excel(path_data + 'RFDM2011IRI.xls', sheetname=1) #using int cause name of sheetname have some "é"
# creating header from file
header = revenu_menage.loc[5].tolist()
revenu_menage.columns = header
revenu_menage.rename(columns={'IRIS':'CODGEO'}, inplace=True)
# to get real values
revenu_menage = revenu_menage[6:]
# creating new feature : sum of all feature
features = [x for x in header if x not in ['IRIS','LIBIRIS','COM','LIBCOM','REG','DEP','ARR','CV','ZE2010']] # special list for this file
# No need to sum features here (% and quantile)
features.append('CODGEO')
print("il y a  %d iris différentes pour le revenu par ménage et %d features" % (len(revenu_menage.CODGEO.unique()), len(features) - 1))

data = pd.merge(data, revenu_menage[features], on='CODGEO', how='outer')

## Revenu par personne
revenu_personne = pd.read_excel(path_data+'RFDP2011IRI.xls', sheetname=1) #using int cause name of sheetname have some "é"
# creating header from file
header = revenu_personne.loc[5].tolist()
revenu_personne.columns = header
revenu_personne.rename(columns={'IRIS':'CODGEO'}, inplace=True)
# to get real values
revenu_personne = revenu_personne[6:]
# creating new feature : sum of all feature
features = [x for x in header if x not in ['IRIS','LIBIRIS','COM','LIBCOM','REG','DEP','ARR','CV','ZE2010']] # special list for this file
# No need to sum features here (% and quantile)
features.append('CODGEO')
print("il y a  %d iris différentes pour le revenu par personne et %d features" % (len(revenu_personne.CODGEO.unique()), len(features) - 1))

data = pd.merge(data, revenu_personne[features], on='CODGEO', how='outer')


## Revenu par unité de consomation
revenu_uc = pd.read_excel(path_data+'RFDU2011IRI.xls', sheetname=1) #using int cause name of sheetname have some "é"
# creating header from file
header = revenu_uc.loc[5].tolist()
revenu_uc.columns = header
revenu_uc.rename(columns={'IRIS':'CODGEO'}, inplace=True)
# to get real values
revenu_uc = revenu_uc[6:]
# creating new feature : sum of all feature
features = [x for x in header if x not in ['IRIS','LIBIRIS','COM','LIBCOM','REG','DEP','ARR','CV','ZE2010']] # special list for this file
# No need to sum features here (% and quantile)
features.append('CODGEO')
print("il y a  %d iris différentes pour le revenu par unité de consomation et %d features" % (len(revenu_uc.CODGEO.unique()), len(features) - 1))

data = pd.merge(data, revenu_uc[features], on='CODGEO', how='outer')

## Revenu % imposé + détails (% ménage imposé, dont traitement salaire etc..)
revenu_impose = pd.read_excel(path_data+'RFST2011IRI.xls', sheetname=1) #using int cause name of sheetname have some "é"
# creating header from file
header = revenu_impose.loc[5].tolist()
revenu_impose.columns = header
revenu_impose.rename(columns={'IRIS':'CODGEO'}, inplace=True)
# to get real values
revenu_impose = revenu_impose[6:]
# creating new feature : sum of all feature
features = [x for x in header if x not in ['IRIS','LIBIRIS','COM','LIBCOM','REG','DEP','ARR','CV','ZE2010']] # special list for this file
# No need to sum features here (% and quantile)
features.append('CODGEO')
print("il y a  %d iris différentes pour le revenu par ménage imposé et %d features" % (len(revenu_impose.CODGEO.unique()), len(features) - 1))

data = pd.merge(data, revenu_impose[features], on='CODGEO', how='outer')

### Fin de revenu
#-------------------------------------------------------------------------


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
