# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 12:45:22 2015

@author: Florian, Alexis
"""

import pandas as pd

##################### IMPORT DES DONNEES COMMUNES ############################

#
#def read_from_csv()
#
#
#    # -- Keep &  Drop columns
#    agg_cols = ['CODGEO', 'LIBGEO', 'COM', 'LIBCOM', 'REG', 'DEP', 'ARR',
#                'CV', 'ZE2010', 'UU2010', 'UU12010', 'ID_MODIF_GEO']
#
#    path = r'D:\Data\base_commune\CSV'
##    files = glob.glob(path + "/*.csv")
##    dict_dtypes = {'CODGEO': str,
##                   'DEP': str}
##    df1 = pd.read_csv(files[0], dtype=dict_dtypes)
#
#
#    df1 = df1[df1.DEP == '60']
#    # Initialisation du df + key pour le merge
#    t_communes = pd.DataFrame()
#    t_communes['CODGEO'] = df1.CODGEO
#
#    for f in files:
#        df = pd.read_csv(f, dtype=dict_dtypes)
#        # -- Oise
#        df = df[df.DEP == '60']
#        # -- Drop useless cols
#        drop = [x for x in df.columns if x in drop_cols]
#        df.drop(drop, inplace=True, axis=1)
#        # -- Calcul des indicateurs nb_...
#        features = [x for x in df.columns if x not in agg_cols]
#        try:  # Si l'item est dans le dict
#            var = file_dict[f]
#            if var in ['nb_enseignement_1', 'nb_enseignement_2']:
#                df[var] = sum_features(df, file_spe[var])
#            else:
#                df[var] = sum_features(df, features)
#        except KeyError:
#            print(str(f.split('\\')[4]) + '   => No sum for this table')
#            pass
#        t_communes = pd.merge(t_communes, df, on='CODGEO', how='outer')
#
#    t_communes = t_communes.rename(columns={'CODGEO': 'COM'})
#
#    return t_communes

##################### IMPORT DES DONNEES IRIS ############################


''' Import des données IRIS grâce à l'open-moulinette'''
print("Initialisation...")

path = 'data/'

key = ['CODGEO', 'LIBGEO', 'COM', 'LIBCOM', 'REG', 'DEP', 'UU2010']

columns_not_to_sum = ['CODGEO', 'LIBGEO', 'COM', 'LIBCOM', 'REG', 'DEP', 'ARR',
                      'CV', 'ZE2010', 'UU2010', 'UU12010', 'ID_MODIF_GEO']


def _read_iris_file(filename):
    return pd.read_excel(path + filename + '.xls', sheetname='IRIS')


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
    commerce = ('equip-serv-commerce-infra', None),
    sport = ('equip-sport-loisir-socio-infra-13',
             ['NB_F101', 'NB_F102', 'NB_F103', 'NB_F104',
              'NB_F105', 'NB_F106', 'NB_F107', 'NB_F108',
              'NB_F109', 'NB_F110', 'NB_F111', 'NB_F112',
              'NB_F113', 'NB_F114', 'NB_F115', 'NB_F117', 'NB_F118']),
    enseignement_degre_1 = ('equip-serv-ens-1er-degre-infra',
                            ['NB_C101', 'NB_C102', 'NB_C104', 'NB_C105']),
    enseignement_degre_2 = ('equip-serv-ens-2eme-degre-infra',
                            ['NB_C201', 'NB_C301', 'NB_C302', 'NB_C303',
                             'NB_C304', 'NB_C305']),
    enseignement_sup = ('equip-serv-ens-sup-form-serv-infra',
                        ['NB_C401', 'NB_C402', 'NB_C403',
                         'NB_C409', 'NB_C501', 'NB_C502',
                         'NB_C503', 'NB_C504', 'NB_C509',
                         'NB_C601', 'NB_C602', 'NB_C603',
                         'NB_C604', 'NB_C605', 'NB_C609',
                         'NB_C701', 'NB_C702']),
    social = ('equip-serv-action-sociale-infra', None),
    sante = ('equip-serv-sante-infra', None),
    medical = ('equip-serv-medical-para-infra', None),
    service_particulier = ('equip-serv-particuliers-infra', None),
    transport_tourisme = ('equip-tour-transp-infra', None),
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
revenu_menage = pd.read_excel(path + 'RFDM2011IRI.xls', sheetname=1) #using int cause name of sheetname have some "é"
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
revenu_personne = pd.read_excel(path+'RFDP2011IRI.xls', sheetname=1) #using int cause name of sheetname have some "é"
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
revenu_uc = pd.read_excel(path+'RFDU2011IRI.xls', sheetname=1) #using int cause name of sheetname have some "é"
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
revenu_impose = pd.read_excel(path+'RFST2011IRI.xls', sheetname=1) #using int cause name of sheetname have some "é"
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
logement = pd.read_excel(path+'base-ic-logement-2011.xls', sheetname='IRIS')
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
diplome = pd.read_excel(path+'base-ic-diplomes-formation-2011.xls', sheetname='IRIS')
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
famille = pd.read_excel(path+'base-ic-couples-familles-menages-2011.xls', sheetname='IRIS')
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
population = pd.read_excel(path+'base-ic-evol-struct-pop-2011.xls', sheetname='IRIS')
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
activite = pd.read_excel(path+'base-ic-activite-residents-2011.xls', sheetname='IRIS')
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