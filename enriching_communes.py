import pandas as pd

from utils import dict_to_df_list
from insee_millesime_links import COMMUNES

from insee_millesime_lookup import (
    cantons, arrondissements, department, region
)
##
communes = (
    pd
    ## Stacking year dataset for communes
    .concat(
        dict_to_df_list(COMMUNES,['COM','REG','DEP','CAN','ARR'])
    )
    ## Grouping by to yield a list of years where the 
    ## attributes combination was effective
    .groupby(['COM','REG','DEP','CAN','ARR'])
    ['YEAR']
    .apply(list)
    .reset_index()
    ## One row per year per attributes
    .explode('YEAR')
    ## Enriching with labels
    .merge(cantons        , on = ['CAN','YEAR'], how = 'left')
    .merge(arrondissements, on = ['ARR','YEAR'], how = 'left')
    .merge(department     , on = ['DEP','YEAR'], how = 'left')
    .merge(region         , on = ['REG','YEAR'], how = 'left')
    ## Pivoting
    .assign(DUMMY = True)
)
