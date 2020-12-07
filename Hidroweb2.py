# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 12:00:55 2020

@author: bruno
"""

import pandas as pd
import datetime as dt
from calendar import monthrange

est = "chuvas_C_02346041"
path1 = "C:/Users/bruno/GDrive@gmail/0 - Re-mov/0 - Est&Id/5 Git/51 arruma_dados/" + est + ".csv"
path2 = "C:/Users/bruno/GDrive@gmail/0 - Re-mov/0 - Est&Id/5 Git/51 arruma_dados/" + est +"_int.csv"
path3 = "C:/Users/bruno/GDrive@gmail/0 - Re-mov/0 - Est&Id/5 Git/51 arruma_dados/" + est +"_transp.csv"
path4 = "C:/Users/bruno/GDrive@gmail/0 - Re-mov/0 - Est&Id/5 Git/51 arruma_dados/" + est +"_precip.csv"

# dropando linhas e colunas que não vamos usar

df1 = pd.read_csv(path1, sep=';', encoding='windows-1252', header=8, skipinitialspace=True, index_col=False, skiprows=(0), decimal=',', thousands='.')
to_drop =[0,3,4,5,6,7,8,9,10,11,12,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74]
df1.drop(df1.columns[to_drop], axis=1, inplace=True)
df2 = df1.drop(df1.columns[[0,1]], axis=1, inplace=False)

# arrumando datas

datas = pd.to_datetime(df1['Data'], format="%d/%m/%Y")
dia = min(datas)
ultimo_dia = max(datas)

# extraindo quantidade de dias por semana 

ano = pd.DatetimeIndex(datas).year
mes = pd.DatetimeIndex(datas).month
dias_mes = []
x=0
while x < len(datas):  
    dias_mes.append(monthrange(ano[x],mes[x])[1])
    x+=1
    
n_dias = pd.DataFrame({'data':     datas,
                       'dias_mes': dias_mes
                       })

# criando série de dias
 
dias=[]

for dia in pd.date_range(min(datas),max(datas)):
    dia += dt.timedelta(days=1)
    dias.append(dia)

#criando df com coluna de dias e coluna com precipitações


len(precip)
len(dias)

precip2 =[]

for y in len(datas):
    for x in x precip2.append()

precip = df2.stack(level=-1, dropna=False)

dados = {'Data':  dias,
        'Precipitacao': precip
        }

df3 = pd.DataFrame(dados)

df1.to_csv(path2,sep=';', decimal=',',index = False)
df3.to_csv(path3,sep=';', decimal=',',index = False)
precip.to_csv(path4,sep=';', decimal=',',index = False)


