# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 18:14:48 2023

@author: Marina
"""
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Funció que, donat una referència de producte, calcula el nombre total de 
# proveedors que treballen amb ell. A més pot fer un plot per visualitzar les
# dates en les que cada proveedor ha treballat amb el producte, a quin magatzem
# l'ha enviat i quin volum de producte va comprar
def provsxproducto(ref_prod, df, do_plot = True):
    aux_pos = df[['proveedor','producto']]
    aux_pos = (aux_pos.groupby(['producto'])
               .nunique()
               .drop('producto', axis=1)
               .reset_index())
    
    if ref_prod in aux_pos['producto'].values:
        print('** Número de proveedores del producto',ref_prod,'**')
        print(int(aux_pos[aux_pos['producto']==ref_prod]['proveedor']),
              'proveedores. ID:', 
              list(df[df['producto']==ref_prod]['proveedor'].unique()))
        prod = df[df['producto'] == ref_prod]
        
        if do_plot:
            fig, ax = plt.subplots(1, 1, figsize=(15, 8))
            sns.scatterplot(data=prod, x='fecha_emision',y='proveedor', 
                            hue='almacen', size = 'catidad_solicitada',
                            sizes = (50,500), palette='crest')
            ax.tick_params(axis='x', rotation=90)
            plt.ylabel("ID proveedor")
            plt.title("Historico proveedor por producto '{0}'".format(ref_prod),
                      fontsize=20)
            plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
            
    else:
        print('La referencia introducida no está en la base de datos POs')
        
# Funció que donat un df, genera un diccionari on les keys son els proveedors
# i els valors un segon diccionari que conté la data inici, final i el volum
# de productes dels moviments de cada proveedor.
def dic_provxtiempos(df):
    d_prov = {}
    prov = list(df['proveedor'])
    vol = [0]*len(prov)
    for p in range(len(prov)):
        fechas = list(df[df['proveedor']==prov[p]]['fecha_emision'])
        vol[p] += sum(list(df[df['proveedor']==prov[p]]['catidad_solicitada']))
        d_prov[prov[p]] = {'first':min(fechas), 'last':max(fechas),
                           'vol': vol[p]}
    return d_prov

# Funció que usant el diccionari de la funció `dic_provxtiempos()` separa en
# dos dic els proveedors que considera que treballen de manera simultànea
# (entre la data inici i la data fi del proveedor, treballen altres proveedors)
# o de manera única.
def sep_simultaneos(dic):
    uni_prov = {}
    multi_prov = {}

    keys = list(dic.keys())
    total_keys = len(keys)

    for i, key in enumerate(list(dic.keys())):
        act_last_date = dic[key]['last']

        if i == total_keys - 1:
            act_first_date = dic[key]['first']
            if (act_first_date > dic[keys[i]]['first']):
                uni_prov.setdefault(key, 0)
                uni_prov[key] += dic[key]['vol']
            else:
                multi_prov.setdefault(key, 0)
                multi_prov[key] += dic[key]['vol']
        else:
            seg_first_date = dic[keys[i+1]]['first']
            if act_last_date < seg_first_date:
                uni_prov.setdefault(key, 0)
                uni_prov[key] += dic[key]['vol']
            else:
                multi_prov.setdefault(key, 0)
                multi_prov[key] += dic[key]['vol']

    return uni_prov, multi_prov

# Mètrica que calcula el nombre de proveedors que treballen en sobre un
# producte segons si s'han classificat com a multiproveedor o uniproveedor.
def calculo_multi_prov(dic1,dic2):
    if(len(dic2)>0):
        values = np.array(list(dic2.values()))
        valor_esp = np.mean(values)
        n_prov = len(dic2)-sum((valor_esp-(values/len(dic2))))/np.sum(values)
        if (len(dic1)>0):
            return np.mean([1,n_prov])
        else:
            return n_prov
    else:
        return 1
   
# Funció que forma el procés per, donat un dataset, calcular el nombre de 
# proveedors simultanis per producte.
def generar_multiprov_id(df):
    d_prova = dic_provxtiempos(df)
    u, m = sep_simultaneos(d_prova)
    return calculo_multi_prov(u, m)