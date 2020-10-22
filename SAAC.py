# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 19:33:36 2020

@author: Ligia e Brunis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

#@title Entrada de dados pelo usuário { display-mode: "form" }
area =  100#@param {type:"number"}
volume_maximo =  2000#@param {type:"integer"}
intervalo_volumes =  500#@param {type:"integer"}
coeficiente = 0.8 #@param ["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1"] {type:"raw"}
demanda =  80#@param {type:"number"}
potencial_substituicao = 1 #@param ["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1"] {type:"raw"}
diferenca_economia = 0.1 #@param {type:"number"}

volume = list(range(0,volume_maximo,intervalo_volumes))

chuva = pd.read_csv("D:/Git/Dimensionamento-SAAC/P_Sofia.csv")

calculos = pd.DataFrame(chuva)

calculos['Vcaptado'] = calculos.P * area * coeficiente
calculos['Vinicio'] = 0.00
calculos['Vfim'] = 0.00
calculos['Vconsumido'] = 0.00
calculos['Epot'] = 0.00
Epot_media = []
potencial_utilizacao = []
variacao_potencial = []

for j in range(0, len(volume), 1):

    for i in range(1, len(calculos), 1):

        calculos.Vinicio[i] = min(calculos.Vfim[i-1] + calculos.Vcaptado[i], volume[j])
        calculos.Vconsumido[i] = min(calculos.Vinicio[i], demanda)
        calculos.Vfim[i] = calculos.Vinicio[i] - calculos.Vconsumido[i]
        calculos.Epot[i] = calculos.Vconsumido[i] / demanda * 100
    print(j)
         
    Epot_media.append(calculos.Epot.mean())
    potencial_utilizacao.append(calculos.Epot.mean() / potencial_substituicao)
  
resultados = pd.DataFrame(columns=['Volume', 'Ppluv'], index=None)
resultados.Volume = volume
resultados.Ppluv = potencial_utilizacao

for k in range(1, len(volume), 1):

    variacao = (potencial_utilizacao[k] - potencial_utilizacao [k-1]) / (intervalo_volumes / 1000)
    variacao_potencial.append(variacao)

    if variacao <= diferenca_economia * 100:
        volume_ideal = volume[k]
        potencial = potencial_utilizacao[k]
        break

plt.plot(resultados.Volume, resultados.Ppluv, '-ok', color='black');
plt.plot(volume_ideal, potencial, 'o', color='red')

plt.xlim(0, volume_maximo);
plt.ylim(0, 100);

plt.xlabel('Volume do reservatório (L)')
plt.ylabel('Potencial de economia de água potável (%)');
plt.title('Resultados da simulação', fontsize=20)

plt.show()

print('Volume ideal do reservatório: ', volume_ideal, ' m³')
print('Potencial de utilização de água pluvial: {:.2f}%'.format(potencial))