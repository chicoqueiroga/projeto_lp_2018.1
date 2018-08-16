# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


def pegaDfProcon(ano):
	trimestres = np.arange(1,5)
	caminhos = map(lambda trimestre: "../../../Data/Atendimentos Fornecedor/"+ano+"/Trimestre "+str(trimestre)+".csv", trimestres)
	myDfsTrimestre = map(lambda caminho: pd.read_csv(caminho, delimiter=';', na_filter=False, error_bad_lines=False), caminhos)

	myDf =  pd.concat(myDfsTrimestre)
	myDf = myDf[
    (myDf.CodigoCNAEPrincipal != 'NULL') &\
	(myDf.DescricaoTipoAtendimento.isin(['Abertura Direta de Reclamação', 'Reclamação de Ofício']))]

	myDf['GrupoProblema'] = myDf['GrupoProblema'].apply(lambda x : x.replace('Problemas', 'P.') if 'Problemas' in x else (x.replace(' de Produto ou Serviço', '') if 'Serviço' in x else x))

	return myDf