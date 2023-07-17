# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 15:09:51 2023

@author: Marina
"""
import pandas as pd
import missingno as msno
from IPython.display import display


# Funció per llegir un df donat un path
def read_df(df_path):
    return pd.read_csv(df_path)

def count_null_values(df):
    print(pd.isnull(df).values.sum(),'entradas nulas,'\
          ' correspondientes a un {:.2f}% de los valores en el df'.format(pd.isnull(df).values.sum()*100/df.size))
    
def count_duplicate_rows(df):
    n = df.duplicated().sum()
    print('Número de filas duplicadas: ', n)
    return n
    
def delete_duplicate_rows(df):
    df.drop_duplicates(subset=None,keep="first",inplace=True)
    return df
    
def plot_null_matrix(df):
    return msno.matrix(df,figsize=(5,4),fontsize=10)

# Funció per fer una vista ràpida d'un df. Mira els valors null i les entrades
# duplicades. Per defecte adjunta un plot per visualitzar on estan localitzats
# els nulls (per canviar-ho entrar do_plot=False) i si la funció s'iguala a una
# variable, aquesta contindra el df entrat sense valors repetits (si en té).    
def visualitzacio_df(df):
    print('Columns:',list(df.columns))
    display(df)
    count_null_values(df)
    plot_null_matrix(df)
    n = count_duplicate_rows(df)
    if n != 0:
        delete_duplicate_rows(df)
    
