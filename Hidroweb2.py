# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 12:00:55 2020

@author: bruno
"""

import pandas as pd
import datetime as dt
from calendar import monthrange

est = "chuvas_C_02346041.csv"
path = "C:/Users/bruno/GDrive@gmail/0 - Re-mov/0 - Est&Id/5 Git/51 arruma_dados/" + est
exp = path + "_export"

df1 = pd.read_csv(path, sep=';', encoding='windows-1252', header=8, index_col=False, decimal=',', thousands='.')
df1['Data']=pd.to_datetime(df1['Data'], format="%d/%m/%Y")

df1=df1.assign(**{'ano': pd.DatetimeIndex(df1['Data']).year,
                  'mes': pd.DatetimeIndex(df1['Data']).month})
df1.insert(len(df1.columns),'n_dias',[monthrange(df1['ano'][x],df1['mes'][x])[1] for x in range(len(df1['Data']))])

# ordenando chuvas 

precip =[]
lin=0
col_i=df1.columns.get_loc('Chuva01')

for lin in range(len(df1['Data'])):                     
    for col in range(col_i,df1['n_dias'][lin]+col_i):
        precip.append(df1.iloc[lin][col])
    lin+=1
    
# ordenando dias, considerando que há anos < 12 meses

dias=[]
dias.append(min(df1['Datas']))
lin=0

for lin in range(len(df1['Data'])):
    for dia in range(df1['n_dias'][lin]):
        dias.append(df1['Data'][lin]+dt.timedelta(days=dia))
    lin+=1

# juntando e exportando

df2 = pd.DataFrame({'Data':        dias,
                   'Chuva_mm_dia': precip})

df2.to_csv(exp+'.csv', sep=';',index=False, decimal=',',header=False)

'''
# análises

meses_serie_real = df1['Data'].groupby(by=df1['Data'].dt.year).count()
meses_serie_ideal
dias_serie_real =
dias_serie_ideal =
registros_real =
registros_ideal =

dias_seq=[]

for dia in pd.date_range(min(df1['Data']),max(df1['Data'])):
    dias_seq.append(min(df1['Data'])+dt.timedelta(days=1))
'''

'''
# baixar arquivo
# colocar jeito de selecionar arquivo
'''