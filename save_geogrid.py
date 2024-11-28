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

## Enriching
dff = (
    df
    .merge(
        communes,
        on = 'COM',
        how = 'left'
    )
    .drop_duplicates()
)

## Handling PARIS / LYON / MARSEILLE
plm = (
    postcode
    .loc[lambda d: d.COM.str.startswith(('132','693','751'))]
    .assign(
        NCC = lambda d: np.select(
            [d.COM.str.startswith('693'),
             d.COM.str.startswith('751'),
             d.COM.str.startswith('132')],
            ['LYON',
             'PARIS',
             'MARSEILLE']
        )
    )
    .merge(
        dff
        .drop(['COM','CODE_POSTAL_2024','GPS_COORDINATES_2024'],axis=1),
        on = 'NCC'
    )
    .drop_duplicates()
)

for y in [2020,2021,2022,2023,2024]:
    plm[f'CODE_INSEE_{y}'] = plm.COM
    plm[f'{y}'] = True

## Saving
(
    pd
    .concat([dff,plm])
    .to_csv('GEOGRID.csv',sep = ';',index = False)
)

## examples:
#dff.loc[lambda d: d.COM.isin(['01039','01138'])]