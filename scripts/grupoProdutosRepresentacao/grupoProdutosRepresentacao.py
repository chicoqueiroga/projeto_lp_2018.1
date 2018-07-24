# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

proconCsvFile1 = "../../../Data/Atendimentos Fornecedor/2017/Trimestre 1.csv"

"""proconDt1 = pd.read_csv(proconCsvFile1, delimiter = ';', na_filter = False)
proconCsvFile2 = "../../../Data/Atendimentos Fornecedor/2017/Trimestre 2.csv"
proconDt2 = pd.read_csv(proconCsvFile2, delimiter = ';', na_filter = False)
proconCsvFile3 = "../../../Data/Atendimentos Fornecedor/2017/Trimestre 3.csv"
proconDt3 = pd.read_csv(proconCsvFile3, delimiter = ';', na_filter = False)
proconCsvFile4 = "../../../Data/Atendimentos Fornecedor/2017/Trimestre 4.csv"
proconDt4 = pd.read_csv(proconCsvFile4, delimiter = ';', na_filter = False)

proconDt = pd.concat([proconDt1, proconDt2, proconDt3, proconDt4])
"""

proconDt = pd.read_csv(proconCsvFile1, delimiter = ';', na_filter = False)
proconDt = proconDt[
    (proconDt.CodigoCNAEPrincipal != 'NULL') &\
	(proconDt.DescricaoTipoAtendimento.isin(['Abertura Direta de Reclamação', 'Reclamação de Ofício']))]


proconDt['GrupoProblema'] = proconDt['GrupoProblema'].apply(lambda x : x.replace('Problemas', 'P.') if 'Problemas' in x else x)
proconDt['GrupoProblema'] = proconDt['GrupoProblema'].apply(lambda x : x.replace(' de Produto ou Serviço', '') if 'Serviço' in x else x)

def analiseDePareto(coluna):
	dfAnalisado = pd.Series.to_frame(proconDt[coluna].value_counts())
	dfAnalisado.reset_index(inplace=True)
	dfAnalisado.columns = [coluna, 'qtdOcorrencia']
	dfAnalisado.sort_values('qtdOcorrencia')
	dfAnalisado['porcentagem'] = (dfAnalisado['qtdOcorrencia'] / dfAnalisado['qtdOcorrencia'].sum()) * 100
	dfAnalisado['porcentagemAcumulada'] = dfAnalisado['porcentagem'].cumsum()

	outrosDt = dfAnalisado[dfAnalisado.porcentagemAcumulada > 80]
	dfAnalisado = dfAnalisado[dfAnalisado.porcentagemAcumulada <= 80]
	dfAnalisado = dfAnalisado[[coluna, 'qtdOcorrencia', 'porcentagemAcumulada']]

	dfAnalisado = dfAnalisado.append({coluna: 'Outros', 'qtdOcorrencia': outrosDt.qtdOcorrencia.sum(), 'porcentagemAcumulada': 100}, ignore_index=True)

	dfAnalisado.set_index(coluna, inplace=True)

	barras = dfAnalisado.qtdOcorrencia.plot(kind='bar', color='r')
	linha  = dfAnalisado.porcentagemAcumulada.plot(linestyle='-', marker='o', ax=barras, secondary_y=True, color = '#008000', rot=85)
	linha.set_yticks(np.arange(0,101,10))

	plt.savefig(coluna + ' Completo.png', bbox_inches='tight')
	plt.show()
	return list(dfAnalisado.index.values)


principaisProdutosServicos = analiseDePareto('GrupoAssunto')
principaisProblemas = analiseDePareto('GrupoProblema')

agrupamento = proconDt[proconDt.GrupoAssunto.isin(principaisProdutosServicos)].groupby('GrupoAssunto')['GrupoProblema'].value_counts()

outrosProblemas = agrupamento[~agrupamento.index.get_level_values('GrupoProblema').isin(principaisProblemas)]
outrosProblemas = outrosProblemas.unstack(level=-1, fill_value=0)

outrosProblemas['Outros Problemas'] = outrosProblemas.sum(axis=1)


outrosProblemas = pd.Series.to_frame(outrosProblemas['Outros Problemas'])
outrosProblemas = outrosProblemas.stack()

agrupamento = agrupamento[agrupamento.index.get_level_values('GrupoProblema').isin(principaisProblemas)]
agrupamento = pd.concat([agrupamento, outrosProblemas])

print(type(agrupamento))

# agrupamento.columns = ['qtdOcorrencia']

agrupamento = agrupamento.unstack(level=-1, fill_value=0)
agrupamento['totalOcorrencias'] = agrupamento.sum(axis=1)

agrupamento.sort_values('totalOcorrencias', inplace=True)
agrupamento.drop(columns = ['totalOcorrencias'], inplace=True)

agrupamento.plot.barh(stacked=True)

plt.savefig('agrupamento.png', bbox_inches='tight')
plt.show()