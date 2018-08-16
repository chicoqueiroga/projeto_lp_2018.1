# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import sys
sys.path.insert(0, '../utils/')
from utils import pegaDfProcon

def analiseDePareto(coluna, ano, df):
	dfAnalisado = pd.Series.to_frame(df[coluna].value_counts())
	dfAnalisado.reset_index(inplace=True)
	dfAnalisado.columns = [coluna, 'qtdOcorrencia']
	dfAnalisado.sort_values('qtdOcorrencia')
	dfAnalisado['porcentagem'] = (dfAnalisado['qtdOcorrencia'] / dfAnalisado['qtdOcorrencia'].sum()) * 100
	dfAnalisado['porcentagemAcumulada'] = dfAnalisado['porcentagem'].cumsum()

	outrosDf = dfAnalisado[dfAnalisado.porcentagemAcumulada > 80]
	dfAnalisado = dfAnalisado[dfAnalisado.porcentagemAcumulada <= 80]
	dfAnalisado = dfAnalisado[[coluna, 'qtdOcorrencia', 'porcentagemAcumulada']]
	dfAnalisado = dfAnalisado.append({coluna: 'Outros', 'qtdOcorrencia': outrosDf.qtdOcorrencia.sum(), 'porcentagemAcumulada': 100}, ignore_index=True)
	dfAnalisado.set_index(coluna, inplace=True)

	barras = dfAnalisado.qtdOcorrencia.plot(kind='bar', color='r')
	linha  = dfAnalisado.porcentagemAcumulada.plot(linestyle='-', marker='o', ax=barras, secondary_y=True, color = '#008000', rot=90)
	linha.set_yticks(np.arange(0,101,10))
	
	plt.savefig(ano + '/' + coluna + ' Pareto.png', bbox_inches='tight')
	plt.show()
	return list(dfAnalisado.index.values)


def representacaoAssuntoProblema(df):
	ano = str(df['AnoAtendimento'].values[0])
	
	principaisProdutosServicos = analiseDePareto('GrupoAssunto', ano, df)
	principaisProblemas = analiseDePareto('GrupoProblema', ano, df)

	agrupamento = df[df.GrupoAssunto.isin(principaisProdutosServicos)].groupby('GrupoAssunto')['GrupoProblema'].value_counts()

	outrosProblemas = agrupamento[~agrupamento.index.get_level_values('GrupoProblema').isin(principaisProblemas)]
	outrosProblemas = outrosProblemas.unstack(level=-1, fill_value=0)

	outrosProblemas['Outros Problemas'] = outrosProblemas.sum(axis=1)

	outrosProblemas = pd.Series.to_frame(outrosProblemas['Outros Problemas'])
	outrosProblemas = outrosProblemas.stack()

	agrupamento = agrupamento[agrupamento.index.get_level_values('GrupoProblema').isin(principaisProblemas)]
	agrupamento = pd.concat([agrupamento, outrosProblemas])

	agrupamento = agrupamento.unstack(level=-1, fill_value=0)
	agrupamento['totalOcorrencias'] = agrupamento.sum(axis=1)

	agrupamento.sort_values('totalOcorrencias', inplace=True)
	agrupamento.drop(columns = ['totalOcorrencias'], inplace=True)

	agrupamento.plot.barh(stacked=True, legend=True)

	myCursor = Cursor(ax, useblit=True, linewidth=2)

	plt.savefig(ano + '/representacaoAssuntoProblema.png', bbox_inches='tight')
	plt.show()

	return agrupamento


def cascata(antesDepois):
	totalAntes = antesDepois[0]['Vício ou Má Qualidade'].sum()
	totalDepois = antesDepois[1]['Vício ou Má Qualidade'].sum()

	antes = pd.Series.to_frame(antesDepois[0]['Vício ou Má Qualidade'].tail(10))
	depois = pd.Series.to_frame(antesDepois[1]['Vício ou Má Qualidade'])

	antes.columns = ['qtdAnterior']

	antesDepois = antes.join(depois, how='inner')
	antesDepois.rename(columns={'Vício ou Má Qualidade': 'qtdPosterior'}, inplace=True)
	antesDepois['diferenca'] = antesDepois.qtdPosterior - antesDepois.qtdAnterior

	antesDepois = antesDepois['diferenca']
	totalVariacoes = antesDepois.sum()
	variacaoOutros = totalDepois - (totalAntes + totalVariacoes)

	antesDepois['Outros'] = variacaoOutros
	antesDepois = pd.concat([pd.Series(totalAntes, index=['totalAntes']), antesDepois])

	print(type(antesDepois))
	print(antesDepois)

	barraInvisivel = antesDepois.cumsum().shift(1).fillna(0)
	barraInvisivel['totalDepois'] = totalDepois
	antesDepois['totalDepois'] = totalDepois

	passo = barraInvisivel.reset_index(drop=True).repeat(3).shift(-1)
	passo[1::3] = np.nan

	barraInvisivel['totalDepois'] = 0

	my_plot = antesDepois.plot(kind='bar', stacked=True, bottom=barraInvisivel,legend=None)
	my_plot.plot(passo.index, passo.values,'k')

	ax = plt.gca()

	ax.set_ylim(30000, 40000)

	plt.savefig('cascata2016-2017.png', bbox_inches='tight')
	plt.tight_layout()
	plt.show()

anos = ["2014", "2015", "2016", "2017"]

myDfs = map(pegaDfProcon, anos)

agrupamentos = map(representacaoAssuntoProblema, myDfs)
agrupamentos = [(agrupamentos[0], agrupamentos[1]), (agrupamentos[1], agrupamentos[2]), (agrupamentos[2], agrupamentos[3])]

map(cascata, agrupamentos)