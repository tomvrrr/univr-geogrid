import pandas as pd

from insee_millesime_links import *

from utils import dict_to_df_list
from pandas.core.frame import DataFrame as pandas_df


def build_millesime(data:dict, code:str) -> pandas_df:
    '''
    Stack dataframes to generate a table containing the year, code
    of interest and associated labels:
    - NCC: upper name (machine readable) 
    - LIBELLE: Rich name (with accent etc.)

    Variable:
    - data: the dictionnary formatted as {'YEAR':'PATH/URL_TO_DF'}
    - code: Code of interest
    '''
    return (
        pd
        ## Stacking year dataset for communes
        .concat(
            dict_to_df_list(data, [code,'NCC','LIBELLE'])
        )
        .rename(columns={
            'NCC':      f'{code}_NAME_UPPER',
            'LIBELLE':  f'{code}_NAME_RICH'
        })
)


cantons         = build_millesime(CANTONS,'CAN')
arrondissements = build_millesime(ARRONDISSEMENTS,'ARR')
department      = build_millesime(DEPARTMENT,'DEP')
region          = build_millesime(REGION,'REG')