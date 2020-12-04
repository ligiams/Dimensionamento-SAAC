# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 19:33:36 2020

@author: Ligia e Brunis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

#Pedir para o usuário inserir as variáveis básicas:
areaCaptacao = float(input("Insira a área de captação (m²): "))
demandaDiaria = float(input("Insira a demanda diária de usos não potáveis (L): "))

#Pedir para o usuário escolher o tipo de dimensionamento:
opcaoDimensionamento = int(input("Tipo de dimensionamento (1 - Simplificado, 2 - Completo): "))

if (opcaoDimensionamento == 1):
    volumeReservatorio = [0, 240, 600, 700, 1000, 1050, 2500]
    coeficienteEscoamento = 0.8
    potencialSubstituicao = 1
    diferencaEconomia = 0.1

else:
    coeficienteEscoamento = float(input("Insira o coeficiente de escoamento (de 0 a 1): "))
    potencialSubstituicao = float(input("Insira o potencial de substituição (de 0 a 1): "))
    diferencaEconomia = float(input("Insira o diferencial na economia (de 0 a 1): "))
    
    escolhaVolumes = input("Deseja utilizar volumes comerciais (sim ou não)?: ").upper()
    if(escolhaVolumes == "SIM"):
        volumeReservatorio = [0, 240, 600, 700, 1000, 1050, 2500]
    if(escolhaVolumes == "NÃO"):
        volumeMaximo = int(input("Insira o volume máximo (L): "))
        intervaloVolumes = int(input("Insira o intervalo de volumes (L): "))
        volumeReservatorio = list(range(0, volumeMaximo, intervaloVolumes))

# #@title Entrada de dados pelo usuário { display-mode: "form" }
# area =  100#@param {type:"number"}
# volume_maximo =  2000#@param {type:"integer"}
# intervalo_volumes =  500#@param {type:"integer"}
# coeficiente = 0.8 #@param ["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1"] {type:"raw"}
# demanda =  80#@param {type:"number"}
# potencial_substituicao = 1 #@param ["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1"] {type:"raw"}
# diferenca_economia = 0.1 #@param {type:"number"}

# volume = list(range(0,volume_maximo,intervalo_volumes))

chuva = pd.read_csv("D:/Git/Dimensionamento-SAAC/P_Sofia.csv")

calculos = pd.DataFrame(chuva)

calculos['Vcaptado'] = calculos.P * areaCaptacao * coeficienteEscoamento
calculos['Vinicio'] = 0.00
calculos['Vfim'] = 0.00
calculos['Vconsumido'] = 0.00
calculos['Epot'] = 0.00
Epot_media = []
potencialUtilizacao = []
variacaoPotencial = []

for j in range(0, len(volumeReservatorio), 1):

    for i in range(1, len(calculos), 1):

        calculos.Vinicio[i] = min(calculos.Vfim[i-1] + calculos.Vcaptado[i], volumeReservatorio[j])
        calculos.Vconsumido[i] = min(calculos.Vinicio[i], demandaDiaria)
        calculos.Vfim[i] = calculos.Vinicio[i] - calculos.Vconsumido[i]
        calculos.Epot[i] = calculos.Vconsumido[i] / demandaDiaria * 100
         
    Epot_media.append(calculos.Epot.mean())
    potencialUtilizacao.append(calculos.Epot.mean() / potencialSubstituicao)
  
resultados = pd.DataFrame(columns=['Volume', 'Ppluv'], index=None)
resultados.Volume = volumeReservatorio
resultados.Ppluv = potencialUtilizacao

for k in range(1, len(volumeReservatorio), 1):

    variacao = (potencialUtilizacao[k] - potencialUtilizacao [k-1]) / ((volumeReservatorio[k] - volumeReservatorio [k-1]) / 1000)
    variacaoPotencial.append(variacao)

    if variacao <= diferencaEconomia * 100:
        volumeIdeal = volumeReservatorio[k]
        potencial = potencialUtilizacao[k]
        break

plt.plot(resultados.Volume, resultados.Ppluv, '-ok', color='black');
plt.plot(volumeIdeal, potencial, 'o', color='red')

plt.xlim(0, volumeReservatorio[-1]);
plt.ylim(0, 100);

plt.xlabel('Volume do reservatório (L)')
plt.ylabel('Potencial de economia de água potável (%)');
plt.title('Resultados da simulação', fontsize=20)

plt.show()

print('Volume ideal do reservatório: ', volumeIdeal, ' L')
print('Potencial de utilização de água pluvial: {:.2f}%'.format(potencial))