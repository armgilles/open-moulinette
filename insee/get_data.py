# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 10:49:08 2015

@author: Alexis
"""
import os
import zipfile
import pandas as pd

#compatible python 2, python 3 import
try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve


### Données générales
path_insee = 'http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/'
path_data = 'data/'
assert os.path.exists(path_data), 'il faut créer le fichier correspondant à path data'



def download_unzip(url_path, path, names):
    ''' fonction pour aller chercher un zip et pour l'enregistrer dans path
        names est la liste de noms qui doivent être donnés aux fichiers
        Il doit y avoir autant de name dans names que d'objet dans le zip
        téléchargé et les noms doivent être dans l'ordre des fichiers du 
        zip...
    '''
    assert isinstance(names, list)

    filehandle = urlretrieve(url_path)
    assert zipfile.is_zipfile(filehandle[0])
    zip_file_object = zipfile.ZipFile(filehandle[0], 'r')
    assert len(zip_file_object.namelist()) == len(names)
    
    for i, filename in enumerate(zip_file_object.namelist()):
        print('le fichier ' + filename + ' est téléchargé et nommé ' + names[i])
        zip_file_object.extract(filename, path)
        os.rename(os.path.join(path, filename), os.path.join(path, names[i]))
        
#http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/structure-distrib-revenus/structure-distrib-revenus-2011/structure-distrib-revenus-iris-2011.zip
#http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/structure-distrib-revenus/structure-distrib-revenus-2011/structure_distrib_revenus_iris-2011.zip
#http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/structure-distrib-revenus/structure-distrib-revenus-2011/structure-distrib-revenus_iris-2011.zip
##################### IMPORT DES DONNEES COMMUNES ############################

''' Import des données IRIS grâce à l'open-moulinette'''
print("Initialisation...")


key = ['CODGEO', 'LIBGEO', 'COM', 'LIBCOM', 'REG', 'DEP', 'UU2010']

columns_not_to_sum = ['CODGEO', 'LIBGEO', 'COM', 'LIBCOM', 'REG', 'DEP', 'ARR', 'CV',
             'ZE2010', 'UU2010', 'UU12010', 'ID_MODIF_GEO']


def equipement_url(filename):
    url_path = path_insee + filename + '/' + filename + '-infra-13.zip'
    return url_path


def revenu_url(year):
    filename = 'structure-distrib-revenus'
    general_url = path_insee + filename + '/'
    year_folder =  filename + '-' + str(year) + '/'
    zip_name = filename + '-iris-' + str(year) + '.zip'
    return general_url + year_folder + zip_name


def _read_file_or_download(list_filenames, path, url):
    if not isinstance(list_filenames, list):
        list_filenames = [list_filenames]
    # si l'un des fichiers manquent on télécharge
    for filename in list_filenames:    
        path_file_on_disk = path_data + filename
        if not os.path.exists(path_file_on_disk):
            download_unzip(url, path_data, list_filenames)
            break


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


