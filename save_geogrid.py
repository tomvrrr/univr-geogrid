from communes_with_postcode import *
from enriching_communes import *

## 
communes = (
    communes
    .pivot(
        index = [i for i in communes.columns if i not in ['YEAR','DUMMY']],
        columns = 'YEAR',
        values = 'DUMMY'
    )
    .fillna(False)
    .assign(FLAG_CHANGE = lambda d:
            d[['2020','2021','2022','2023','2024']].sum(axis = 1) < 5
    )
    .reset_index()
    
)

## Saving
(
    df
    .merge(
        communes,
        on = 'COM',
        how = 'left')
    .drop_duplicates()
    .to_csv('GEOGRID.csv',sep = ';')
)