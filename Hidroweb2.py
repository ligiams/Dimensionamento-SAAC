# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 12:00:55 2020

@author: bruno and ligiones

Este script carrega um arquivo .csv do Hidroweb e exporta um com apenas duas colunas, uma 
de datas e outra com as chuvas.

"""

import pandas as pd
import datetime as dt
from calendar import monthrange
import tkinter as tk
import os
import sys

# intro caixa de diálogo para escolher arquivo e loop até escolher um csv

while True:
    try:
        print('Selecione um arquivo .csv, por obséquio.')
        root = tk.Tk()
        root.lift()
        root.attributes('-alpha', 0)
        root.attributes('-topmost',True)
        root.after_idle(root.attributes,'-topmost',False)
        chuva_entrada = tk.filedialog.askopenfile(mode='r', title = 'Selecione arquivo csv')    
        root.destroy()
        
        if (chuva_entrada == None): 
            sair = input('\nArquivo de entrada não selecionado. Pressione qualquer tecla para sair.')
            break
            sys.exit()
        else:
            arquivo_entrada = os.path.basename(chuva_entrada.name)
            ext = arquivo_entrada[-4:]       
        if ext == '.csv':
            print('\nTrabalhando...')
            break
        else:
            print('\nArquivo selecionado não é .csv')
    except:
        pass
        
caminho = os.path.dirname(chuva_entrada.name)+'/'
arquivo_saida = arquivo_entrada[:-4]+'_exportado.csv'

# lendo arquivo de entrada e criando df

df1 = pd.read_csv(chuva_entrada.name, sep=';', encoding='windows-1252', header=8, index_col=False, decimal=',', thousands='.')
df1['Data']=pd.to_datetime(df1['Data'], format="%d/%m/%Y")
df1=df1.assign(**{'ano': pd.DatetimeIndex(df1['Data']).year,
                  'mes': pd.DatetimeIndex(df1['Data']).month})
df1.insert(len(df1.columns),'n_dias',[monthrange(df1['ano'][x],df1['mes'][x])[1] for x in range(len(df1['Data']))])

# ordenando chuvas 

precip = []
lin = 0
col_i = df1.columns.get_loc('Chuva01')
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

# juntando no df2 e exportando em csv

df2 = pd.DataFrame({'Data':        dias,
                   'Chuva_mm_dia': precip})

df2.to_csv(caminho+arquivo_saida, sep=';',index=False, decimal=',',header=True)      

# infos sobre o arquivo

data_inicial = min(df1['Data']).strftime('%d-%m-%Y')
data_final = max(df1['Data']).strftime('%d-%m-%Y')
ndias_real = len(dias) 
ndias_ideal = (max(df1['Data'])-min(df1['Data'])).days
ndias_null = df2['Chuva_mm_dia'].isna().sum()
ndias_zero = len([x for x in df2['Chuva_mm_dia'] if x == 0])

# print das infos

print('\n\n################################################################\n\n'
      'GRATILUZ POR USAR O TUCUNARÉ STORMWATER DATA TRANSPOSER 3000 v1.0\n\n'
      'O arquivo exportado foi salvo com sucesso na mesma pasta do arquivo de origem:\n\n'
      '\t- Arquivo original:\t'+ arquivo_entrada +'\n'
      '\t- Arquivo novo:\t\t' + arquivo_saida +'\n'
      '\t- Local:\t\t'+ caminho +'\n\n'+
      'Informações sobre o arquivo:\n\n'
      '\t - Data inicial: '+ data_inicial +'\n'
      '\t - Data final: '+ data_final +'\n'
      '\t - N° de registros: '+ str(ndias_real) +'\n'
      '\t - N° ideal de registros: '+ str(ndias_ideal)+'\n'
      '\t - Dias sem registros: '+str(ndias_ideal-ndias_real)+'\n'
      '\t - Registos nulos :' + str(ndias_null) +'\n'
      '\t - Registros iguais a zero :' + str(ndias_zero))
    
# loop infinito até responder se quer ou não abrir o arquivo exportado e finalização

while True: 
    try:
        resp = str(input('\nVossa excelência gostaria abrir o arquivo exportado? (S/N): ')).lower()
        if resp == 's':
            print('\n>>>>>>> Abrindo arquivo...')
            os.startfile(caminho+arquivo_saida,'edit')
            break
        if resp == 'n':        
            print('\n>>>>>> firmeza entao')
            break
        else:
            print('\n>>>>>> responde direito caraleo. eh "S" ou "N"') 
    except:
        pass

sair = input('\nAperte qualquer tecla para sair... Deus te carregue.')