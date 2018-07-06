# -*- coding: utf-8 -*-
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

brasilShapefile = "../utils/BRUFE250GC_SIR.shp"
brazilGeoDf = gpd.read_file(brasilShapefile)

proconCsvFile1 = "../../../Data/Atendimentos Fornecedor/2017/Trimestre 1.csv"
proconDt1 = pd.read_csv(proconCsvFile1, delimiter = ';', na_filter = False)
proconCsvFile2 = "../../../Data/Atendimentos Fornecedor/2017/Trimestre 2.csv"
proconDt2 = pd.read_csv(proconCsvFile2, delimiter = ';', na_filter = False)
proconCsvFile3 = "../../../Data/Atendimentos Fornecedor/2017/Trimestre 3.csv"
proconDt3 = pd.read_csv(proconCsvFile3, delimiter = ';', na_filter = False)
proconCsvFile4 = "../../../Data/Atendimentos Fornecedor/2017/Trimestre 4.csv"
proconDt4 = pd.read_csv(proconCsvFile4, delimiter = ';', na_filter = False)

proconDt = pd.concat([proconDt1, proconDt2, proconDt3, proconDt4])

estadosCsvFile = "../utils/estadosInfo.csv"
estadosDt = pd.read_csv(estadosCsvFile, delimiter = ';', na_filter = False)

proconDt = proconDt[
    (proconDt.CodigoCNAEPrincipal != 'NULL') &\
	(proconDt.DescricaoTipoAtendimento.isin(['Abertura Direta de Reclamação', 'Reclamação de Ofício'])) &\
	(proconDt.GrupoProblema == 'Problemas na Entrega de Produtos')]

proconDt = pd.Series.to_frame(proconDt['UF'].value_counts())
proconDt.reset_index(level=0, inplace=True)
proconDt.columns = ['UF', 'qtdProblemasEntrega']

joinedEstadosProcon = pd.merge(estadosDt, proconDt, how='inner', on='UF')

brazilDf = pd.DataFrame(brazilGeoDf)
brazilDf['CD_GEOCUF'] = brazilDf['CD_GEOCUF'].apply(int)

brazilDfJoined = pd.merge(brazilDf, joinedEstadosProcon, how='left', on='CD_GEOCUF')
brazilDfJoined['qtdProblemasPorPessoas'] = brazilDfJoined.qtdProblemasEntrega / brazilDfJoined.QTD_PESSOAS

brazilGeoDfJoined = gpd.GeoDataFrame(brazilDfJoined)

brazilGeoDfJoined.plot(column='qtdProblemasPorPessoas', cmap='OrRd')
plt.title('Quantidade relativa de problemas pela densidade demográfica')

brazilGeoDfJoined.plot(column='qtdProblemasEntrega', cmap='OrRd')
plt.title('Quantidade absoluta de problemas')

plt.show()