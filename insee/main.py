# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 09:38:28 2015

"""

from globals import path_data

print("Initialisation...")
from equipements import info_equipement
from revenus import info_revenus
from census import info_population


equipement = info_equipement()
revenu = info_revenus(2011)
population = info_population(2011)

data = equipement.merge(revenu, how='outer')
## petit bout de code pour voir ce qui s'ajoute
#cond = equip_data.CODGEO.isin(revenu.CODGEO)
#equip_data[cond]
#cond = revenu.CODGEO.isin(equip_data.CODGEO)
#revenu[~cond]


data = data.merge(population, how='outer')
## petit bout de code pour voir ce qui s'ajoute
#cond = equip_data.CODGEO.isin(revenu.CODGEO)
#equip_data[cond]
#cond = revenu.CODGEO.isin(equip_data.CODGEO)
#revenu[~cond]

data.to_csv('output.csv')
