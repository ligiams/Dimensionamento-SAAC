# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 12:00:55 2020

@author: bruno
"""

import pandas as pd
import datetime as dt
from calendar import monthrange
import tkinter as tk
from tkinter import filedialog
import os

# caixa de diálogo para escolher arquivo

root = tk.Tk()
root.lift()
root.attributes('-topmost',True)
root.after_idle(root.attributes,'-topmost',False)
chuva_entrada = tk.filedialog.askopenfile(mode='r', title = 'Selecione arquivo')    
root.destroy()
 
if (chuva_entrada == None): 
    sair = input('\tArquivo de entrada não selecionado. \n\t\tPressione enter para sair.\n')
 
caminho = os.path.dirname(chuva_entrada.name)+'/'
arquivo_entrada = os.path.basename(chuva_entrada.name)
arquivo_saida = arquivo_entrada[:-4]+'_saida.csv'

# lendo

df1 = pd.read_csv(chuva_entrada.name, sep=';', encoding='windows-1252', header=8, index_col=False, decimal=',', thousands='.')
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
lin=0

for lin in range(len(df1['Data'])):
    for dia in range(df1['n_dias'][lin]):
        dias.append(df1['Data'][lin]+dt.timedelta(days=dia))
    lin+=1

# juntando e exportando

df2 = pd.DataFrame({'Data':        dias,
                   'Chuva_mm_dia': precip})

df2.to_csv(caminho+arquivo_saida, sep=';',index=False, decimal=',',header=True)

print('\n\n#########\n\nArquivo exportado com sucesso.\n'
      '\tArquivo original:\t'+arquivo_entrada+'\n'
      '\tArquivo novo:\t\t' +arquivo_saida+'\n'
      '\tLocal:\t\t\t\t'+caminho)

