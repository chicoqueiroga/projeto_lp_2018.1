# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

proconCsvFile1 = "../../../Data/Atendimentos Fornecedor/2017/Trimestre 1.csv"

proconDt1 = pd.read_csv(proconCsvFile1, delimiter = ';', na_filter = False)
proconCsvFile2 = "../../../Data/Atendimentos Fornecedor/2017/Trimestre 2.csv"
proconDt2 = pd.read_csv(proconCsvFile2, delimiter = ';', na_filter = False)
proconCsvFile3 = "../../../Data/Atendimentos Fornecedor/2017/Trimestre 3.csv"
proconDt3 = pd.read_csv(proconCsvFile3, delimiter = ';', na_filter = False)
proconCsvFile4 = "../../../Data/Atendimentos Fornecedor/2017/Trimestre 4.csv"
proconDt4 = pd.read_csv(proconCsvFile4, delimiter = ';', na_filter = False)

proconDt = pd.concat([proconDt1, proconDt2, proconDt3, proconDt4])

# proconDt = pd.read_csv(proconCsvFile1, delimiter = ';', na_filter = False)
proconDt = proconDt[
    (proconDt.CodigoCNAEPrincipal != 'NULL') &\
	(proconDt.DescricaoTipoAtendimento.isin(['Abertura Direta de Reclamação', 'Reclamação de Ofício']))]

proconDtAssunto = pd.Series.to_frame(proconDt['GrupoAssunto'].value_counts())
proconDtAssunto.reset_index(inplace=True)
proconDtAssunto.columns = ['Assunto', 'qtdOcorrencia']
proconDtAssunto.sort_values('qtdOcorrencia')
proconDtAssunto['porcentagem'] = (proconDtAssunto['qtdOcorrencia'] / proconDtAssunto['qtdOcorrencia'].sum()) * 100
proconDtAssunto['porcentagemAcumulada'] = proconDtAssunto['porcentagem'].cumsum()

outrosDt = proconDtAssunto[proconDtAssunto.porcentagemAcumulada > 80]
proconDtAssunto = proconDtAssunto[proconDtAssunto.porcentagemAcumulada <= 80]
proconDtAssunto = proconDtAssunto[['Assunto', 'qtdOcorrencia', 'porcentagemAcumulada']]

proconDtAssunto = proconDtAssunto.append({'Assunto': 'Outros', 'qtdOcorrencia': outrosDt.qtdOcorrencia.sum(), 'porcentagemAcumulada': 100}, ignore_index=True)

proconDtAssunto.set_index('Assunto', inplace=True)

print(proconDtAssunto)

barras = proconDtAssunto.qtdOcorrencia.plot(kind='bar', color='r')
linha  = proconDtAssunto.porcentagemAcumulada.plot(linestyle='-', marker='o', ax=barras, secondary_y=True, color = '#008000', rot=90)

plt.savefig('graficoParcial')
plt.savefig('graficoCompleto.png', bbox_inches='tight')
plt.show()