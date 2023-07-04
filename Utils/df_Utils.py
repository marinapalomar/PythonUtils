# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 15:09:51 2023

@author: Marina
"""
import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt
from IPython.display import display


# Funció per llegir un df donat un path
def read_df(df_path):
    return pd.read_csv(df_path)

# Funció per fer una vista ràpida d'un df. Mira els valors null i les entrades
# duplicades. Per defecte adjunta un plot per visualitzar on estan localitzats
# els nulls (per canviar-ho entrar do_plot=False) i si la funció s'iguala a una
# variable, aquesta contindra el df entrat sense valors repetits (si en té).
def visualitzacio_df(df, do_plot=True):
    display(df.head())
    
    print("\n**Número de NaNs**")
    print(pd.isnull(df).values.sum(),'entrades nul·les')
    print('{:.2f}%'.format(pd.isnull(df).values.sum()/df.size*100))
    if (do_plot):
        msno.matrix(df,figsize=(5,4),fontsize=10)
        plt.show()
    
    print("\n**Número dades duplicades**")
    df_copy = df.copy()
    df_copy.drop_duplicates(subset=None,keep="first",inplace=True)
    print('Mida original: ',df.shape,
         '\nNº de dades repetides: ', df.duplicated().sum(),
         '\nMida un cop fet el drop: ',df_copy.shape)
    return df_copy
    del df_copy
    
