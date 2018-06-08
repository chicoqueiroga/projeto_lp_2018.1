# -*- coding: utf-8 -*-
import pandas as pd

planilha = pd.read_csv("dadosabertosatendimentofornecedor4trimestre.csv", delimiter = ';', na_filter = False) 
# print(planilha.columns)
"""
na_values=['not available', 'n.a.', -1] Substitui os valores da lista por NaN
na_values={
		'UF': ['NULL', '0000'],
		'CodigoCNAEPrincipal': ['00', 'NULL', 'null']
		}
"""

planilha[(planilha.UF == 'PE') & (planilha.CodigoCNAEPrincipal != 'NULL') &\
(planilha.DescricaoTipoAtendimento == 'Abertura Direta de Reclamação')].to_csv("pandas.csv",  sep = ';', index = False)
"""
	columns = ['UF', 'CodigoCNAEPrincipal'] Colunas a serem exportadas
"""
#(planilha.DescricaoTipoAtendimento == 'Abertura Direta de Reclamação')
#(planilha.DescricaoTipoAtendimento == 'Reclamação de Ofício')

#6174

from pandas.io import sql
from sqlalchemy import create_engine

tabelaTipo = pd.read_csv('pandas.csv', delimiter = ';', usecols=['DescricaoTipoAtendimento'])
#    skiprows=skip


engine = create_engine('mysql://root:root@localhost/atendimentosPROCON')
with engine.connect() as conn, conn.begin():
    tabelaTipo.to_sql('Tipo', conn, if_exists='append')











# import urllib2

# url = 'http://dados.mj.gov.br/dataset/58f997bf-96e7-4a3e-a8f7-937000f939c7/resource/43a60790-068f-4466-b9fb-5e6514053c1d/download/dadosabertosatendimentofornecedor4trimestre.csv'
# response = urllib2.urlopen(url, timeout = 500000)
# cr = csv.reader(response)

# spamreader = csv.reader(response, delimiter=';')
# for row in spamreader:
# 	print row


####PYTHON 3
# url = 'http://dados.mj.gov.br/dataset/58f997bf-96e7-4a3e-a8f7-937000f939c7/resource/43a60790-068f-4466-b9fb-5e6514053c1d/download/dadosabertosatendimentofornecedor4trimestre.csv'
# from urllib.request import urlopen

# response = urlopen(url)
# CHUNK = 16 * 1024


# with open('file.csv', 'wb') as f:
#     while True:
#         chunk = response.read(CHUNK)
#         if not chunk:
#             break
#         f.write(chunk)

# from __future__ import print_function
# import csv

# dicCabecario = {'UF': 6, 'CEPConsumidor':17, 'NomeFantasiaSindec':20, 'CNPJ': 21, 'CodigoCNAEPrincipal': 25}

# with open('dados.csv', 'rb') as csvfile:
	
# 	arquivoInteiro = csv.reader(csvfile, delimiter=';', quotechar='|')
# 	with open('dadosLimpos.csv', 'w') as f:
# 		for coluna in next(arquivoInteiro):
# 			f.write(coluna + ";")
# 		f.write("\n")

# 		for linha in arquivoInteiro:
# 			dePE = linha[dicCabecario['UF']] == 'PE'
# 			camposNull = linha[dicCabecario['CodigoCNAEPrincipal']] != 'NULL'

# 			if(dePE and camposNull):
# 				for coluna in linha:
# 					f.write("\"" + coluna + "\"" + ";")
# 				f.write("\n")

# url = 'http://dados.mj.gov.br/dataset/58f997bf-96e7-4a3e-a8f7-937000f939c7/resource/43a60790-068f-4466-b9fb-5e6514053c1d/download/dadosabertosatendimentofornecedor4trimestre.csv'
# import requests
# r = requests.get(url, stream=True)
# with open('boaaa.csv', 'wb') as f:
	# for block in r.iter_content(chunk_size=1024):
		# if block:
			# print('.', end="")
			# f.write(block)


# import pandas as pd
# chunksize = 10 ** 8
# for chunk in pd.read_csv(url, chunksize=chunksize):
# 	process(chunk)