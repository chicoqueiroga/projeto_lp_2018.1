# -*- coding: utf-8 -*-
import pandas as pd
from itertools import product
import math
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, '../utils/')
from utils import pegaDfProcon


def pegaDfAnatel(anos):
    caminhos = map(lambda ano: "../../../Data/Reclamacoes Anatel/tabelaAnatel" + str(ano) + ".csv", anos)
    dfsCompletosAno = map(lambda caminho: pd.read_csv(caminho, delimiter=';', na_filter=False, error_bad_lines=False),
                          caminhos)
    myDfsAno = map(lambda df: df[['Ano', 'Mes', 'Servico', 'UF']], dfsCompletosAno)
    myDf = pd.concat(myDfsAno)

    dictSubstituicao = {'Telefone Fixo': 'Telefonia Fixa', 'Banda Larga Fixa': 'Internet',
                        'Celular Pré-Pago': 'Telefonia Celular', 'Celular Pós-Pago': 'Telefonia Celular'}
    myDf = myDf.replace({'Servico': dictSubstituicao})

    myDf['Mes'] = (myDf.Mes / 3.0).apply(lambda x: int(math.ceil(x)))
    myDf.rename(columns={'Mes': 'Trimestre'}, inplace=True)

    return myDf.groupby(['Servico', 'Ano', 'Trimestre'])['UF'].value_counts()

def calculaCorrelacaoLista(tupla):
    coluna = tupla[0]
    lista = tupla[1]
    dataFrame = tupla[2]

    filtradoDf = dataFrame[dataFrame[coluna].isin(lista)]
    correlacao = filtradoDf.QtdProcon.corr(filtradoDf.QtdAnatel)

    return correlacao

def calculaCorrelacao(tupla):
    coluna = tupla[0]
    valor = tupla[1]
    dataFrame = tupla[2]

    filtradoDf = dataFrame[dataFrame[coluna] == valor]
    correlacao = filtradoDf.QtdProcon.corr(filtradoDf.QtdAnatel)

    return correlacao

def correlacaoPorAno(dataFrameCorrelacao):
    anos = list(dataFrameCorrelacao.Ano.unique())
    coluna = ['Ano']
    combinacoes = product(coluna, anos, [dataFrameCorrelacao])

    retorno = map(calculaCorrelacao, combinacoes)
    correlacao = pd.DataFrame(list(retorno), index=anos)
    ax = correlacao.plot(kind='bar', title='Correlacoes por Anos', legend=False, rot=0)
    plt.show()

def correlacaoServicosAtravesAnos(dataFrameCorrelacao):
    servicos = list(dataFrameCorrelacao.Servico.unique())
    coluna = ['Servico']
    combinacoes = product(coluna, servicos, [dataFrameCorrelacao])

    retorno = map(calculaCorrelacao, combinacoes)
    correlacao = pd.DataFrame(list(retorno), index=servicos)
    ax = correlacao.plot(kind='bar', title='Correlacoes por Servicos', legend=False, rot=0)
    plt.show()

def correlacaoRegiaoAtravesAnos(dataFrameCorrelacao):
    nordeste = ['PE', 'PB', 'PI', 'AL', 'BA', 'SE', 'CE', 'MA', 'RN']
    centro_oeste = ['DF', 'MT', 'GO', 'MS']
    sul = ['PR', 'SC', 'RS']
    sudeste = ['MG', 'SP', 'ES', 'RJ']
    norte = ['AM', 'PA', 'RR', 'AC', 'RO', 'TO', 'AP']

    regioes = [nordeste, centro_oeste, sul, sudeste, norte]
    coluna = ['UF']
    combinacoes = product(coluna, regioes, [dataFrameCorrelacao])

    retorno = map(calculaCorrelacaoLista, combinacoes)
    correlacao = pd.DataFrame(list(retorno), index=['NE', 'CO', 'S', 'SE', 'N'])
    ax = correlacao.plot(kind='bar', title='Correlacoes por Regioes', legend=False, rot=0)
    plt.show()

servicos = ['TV por Assinatura', 'Telefonia Celular', 'Telefonia Fixa', 'Internet (Serviços e Produtos)', 'Internet',
            'Internet (Serviços)']
anos = ["2015", "2016", "2017"]
anatelDt = pegaDfAnatel(anos)

myDfs = map(pegaDfProcon, anos)
proconDt = pd.concat(myDfs)

proconDt = proconDt[['AnoAtendimento', 'TrimestreAtendimento', 'GrupoAssunto', 'UF']]
proconDt = proconDt[proconDt.GrupoAssunto.isin(servicos)]
proconDt['GrupoAssunto'] = proconDt['GrupoAssunto'].apply(lambda x: 'Internet' if 'Internet' in x else x)

proconDt.columns = ['Ano', 'Trimestre', 'Servico', 'UF']
proconDt = proconDt.groupby(['Servico', 'Ano', 'Trimestre'])['UF'].value_counts()

proconDt = pd.Series.to_frame(proconDt)
proconDt.columns = ['QtdProcon']

anatelDt = pd.Series.to_frame(anatelDt)
anatelDt.columns = ['QtdAnatel']

correlacaoDt = pd.concat([proconDt, anatelDt], axis=1)
correlacaoDt = correlacaoDt.fillna(0)
correlacaoDt['QtdProcon'] = correlacaoDt['QtdProcon'].apply(int)
correlacaoDt.reset_index(inplace=True)

correlacaoPorAno(correlacaoDt)
correlacaoRegiaoAtravesAnos(correlacaoDt)
correlacaoServicosAtravesAnos(correlacaoDt)