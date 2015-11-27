# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 10:49:08 2015

@author: Alexis
"""
import os
import zipfile

#compatible python 2, python 3 import
try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve


def download_unzip(url_path, path):
    filehandle = urlretrieve(url_path)
    assert zipfile.is_zipfile(filehandle[0])
    zip_file_object = zipfile.ZipFile(filehandle[0], 'r')
    assert len(zip_file_object.namelist()) == 1
    excel_name = zip_file_object.namelist()[0]        
    print('le fichier ' + excel_name + ' est téléchargé' )
    zip_file_object.extract(excel_name, path)
    if 'infra-13' in excel_name:
        new_name = excel_name.replace('infra-13', 'infra')
        os.rename(path + '/' + excel_name, path + '/' + new_name)