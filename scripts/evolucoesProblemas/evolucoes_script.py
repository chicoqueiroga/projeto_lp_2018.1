# coding=utf-8

import pandas as pd
import matplotlib.pyplot as plt
from itertools import product

def calculaComportamentoProblemasTrimestre(arquivo):

    caminhoCompleto = "../../../Data/Atendimentos Fornecedor/" + arquivo

    dadosTrimestre = pd.read_csv(caminhoCompleto, delimiter=';', na_filter=False, error_bad_lines=False)

    atendimentosRequeridos = ["Abertura Direta de Reclamação", "Reclamação de Ofício"]

    dadosTrimestre = dadosTrimestre[(dadosTrimestre.DescricaoCNAEPrincipal != "NULL") & dadosTrimestre.DescricaoTipoAtendimento.isin(atendimentosRequeridos)]
    comportamentoProblemas = dadosTrimestre.GrupoProblema.value_counts()

    print("Fim do processamento do arquivo " + arquivo)

    return comportamentoProblemas

def agrupaComportamentosProblemas(comportamentoAntes, comportamentoDepois):

    evolucao = pd.concat([comportamentoAntes, comportamentoDepois], axis=1, sort=False)

    return evolucao

anos = ["2014", "2015", "2016", "2017"]
trimestres = ["1","2","3","4"]
combinacoes = product(anos, trimestres)

arquivos = map(lambda (ano, numTrimestre): ano + "/Trimestre " + numTrimestre + ".csv", combinacoes)

evolucoesTrimestresSeparados = map(calculaComportamentoProblemasTrimestre, arquivos)
evolucaoCompleta = reduce(agrupaComportamentosProblemas, evolucoesTrimestresSeparados)

evolucaoCompleta = evolucaoCompleta.dropna()
evolucaoCompleta = evolucaoCompleta.transpose()
evolucaoCompleta.index = pd.date_range('01/01/2014', freq = '3MS', periods=16)

print(evolucaoCompleta)

evolucaoCompleta.plot()
#eixos.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()