# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 09:38:29 2020

@author: Ligia
"""

import numpy as np
import pandas as pd
from datetime import datetime

chuva_entrada = pd.read_csv("D:/Git/ChuvaHidroweb/chuvas_C_02346046.csv", sep = ";")
chuva_entrada.Data = pd.to_datetime(chuva_entrada.Data, format="%d/%m/%Y")

chuva_ordenada = chuva_entrada.sort_values(['Data']).reset_index(drop=True)
chuva_ordenada['AnoMes'] = chuva_ordenada.Data.dt.strftime('%Y-%m')


inicio = chuva_ordenada.Data[0]
fim = chuva_ordenada.Data[len(chuva_ordenada)-1]
periodo = 12 * (fim.year - inicio.year) + (fim.month - inicio.month) +1
dias = fim - inicio

datelist = pd.date_range(start=inicio, periods=periodo, freq='M').tolist()

i = 0
datas = []
resultado = []

for data in range(len(datelist)):
    if datelist[data].strftime('%Y-%m') == chuva_ordenada.AnoMes[i]:
        i = i + 1
        for dia in range(1, datelist[data].day+1):
            if dia < 10:
               strdia = str(0) + str(dia)
            else: strdia = str(dia)
            resultado.append(chuva_ordenada['Chuva' + strdia][i-1])
            datas.append(datetime(datelist[data].year, datelist[data].month, dia))
    else:
        for dia in range(1, datelist[data].day+1):
            if dia < 10:
                strdia = str(0) + str(dia)
            else: strdia = str(dia)
            resultado.append('0')
            datas.append(datetime(datelist[data].year, datelist[data].month, dia))
        
chuva = pd.DataFrame()
chuva['Data'] = datas
chuva['Chuva'] = [float(str(s).replace(',','.')) for s in resultado]
chuva['Mes'] = chuva.Data.dt.month
chuva['Ano'] = chuva.Data.dt.year

chuva_mensal = chuva.groupby(['Mes','Ano']).sum()
media_mensal = chuva_mensal.groupby(['Mes'])['Chuva'].mean()