# coding=utf-8

import pandas as pd
import matplotlib.pyplot as plt

evolucaoCompleta = pd.DataFrame()

for ano in range(2014,2018):

    caminhoAno = "../../../Data/Atendimentos Fornecedor/" + str(ano) + "/"

    for numeroTrimestre in range(1,5):

        caminhoTrimestre = caminhoAno + "Trimestre " + str(numeroTrimestre) + ".csv"
        dadosTrimestre = pd.read_csv(caminhoTrimestre, delimiter =';', na_filter = False, error_bad_lines = False)

        atendimentosRequeridos = ["Abertura Direta de Reclamação", "Reclamação de Ofício"]

        dadosTrimestre = dadosTrimestre[(dadosTrimestre.DescricaoCNAEPrincipal != "NULL") & dadosTrimestre.DescricaoTipoAtendimento.isin(atendimentosRequeridos)]
        trimestreSeries = dadosTrimestre.GrupoProblema.value_counts()

        print(trimestreSeries)

        evolucaoCompleta = pd.concat([evolucaoCompleta, trimestreSeries], axis = 1, sort = False)

        print("\nFim do processamento do trimestre \n")

    print("\nFim do processamento do ano \n")

evolucaoCompleta = evolucaoCompleta.dropna()
evolucaoCompleta = evolucaoCompleta.transpose()
evolucaoCompleta.index = pd.date_range('01/01/2014', freq = '3MS', periods=16)

print(evolucaoCompleta)

evolucaoCompleta.plot()
#eixos.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()
