# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 09:39:34 2015

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


def _read_file_or_download(list_filenames, path, url):
    if not isinstance(list_filenames, list):
        list_filenames = [list_filenames]
    # si l'un des fichiers manquent on télécharge
    for filename in list_filenames:
        path_file_on_disk = path_data + filename
        if not os.path.exists(path_file_on_disk):
            download_unzip(url, path_data, list_filenames)
            break