import numpy as np
import pandas as pd

## INSEE: 2020-2024
geocode = (
    pd
    # List of Communes since 1943: https://www.insee.fr/fr/information/7766585
    .read_csv('https://www.insee.fr/fr/statistiques/fichier/7766585/v_commune_depuis_1943.csv',
              dtype=str
    )
    ## Applying correct dtype (date)
    .assign(
        DATE_DEBUT  = lambda d: pd.to_datetime(d.DATE_DEBUT),
        DATE_FIN    = lambda d: pd.to_datetime(d.DATE_FIN)
    )
    ## Excluding commune with changes before 2020
    .loc[lambda d: ~(d.DATE_FIN.dt.year < 2020)]
    .drop_duplicates()
)

## Handling code insee changes
comevnt = (
    pd
    # List of Events 1943: https://www.insee.fr/fr/information/7766585
    .read_csv('https://www.insee.fr/fr/statistiques/fichier/7766585/v_mvt_commune_2024.csv')
    ## Applying correct dtype (date)
    .assign(
        DATE_EFF  = lambda d: pd.to_datetime(d.DATE_EFF)
    )
    ## Excluding commune with changes before 2020
    .loc[lambda d: ~(d.DATE_EFF.dt.year < 2020)]
    ## Finding where insee code changed
    .loc[lambda d: d.COM_AV != d.COM_AP]
    ## Renaming columns
    .rename(columns = {
        'COM_AV':'COM',
        'DATE_EFF':'DATE_FIN',
        'COM_AP':'NEW_COM'
    })
    ## keeping only new/old code insee pair and effective date
    [['COM','DATE_FIN','NEW_COM']]
    .drop_duplicates()
)

## Enriching with new commune code insee after change
df = (
    geocode
    ## Keeping only code insee and validity period
    [['COM','DATE_DEBUT','DATE_FIN']]
    .drop_duplicates()
    .merge(
        comevnt,
        on = ['COM','DATE_FIN'],
        how = 'left'
    )
)

## For each period, create a column 
for i in range(2020,2025):
    df[f'CODE_INSEE_{i}'] = np.select(
        ## 1) if commune exists in year of interest (DEBUT <= YEAR < FIN)
        [(df.DATE_DEBUT.dt.year <= i)&(df.DATE_FIN.dt.year > i),
         (df.DATE_DEBUT.dt.year > i),
         (df.DATE_FIN.dt.year < i),
        ## 2) Or if commune has no 'DATE_FIN'
         df.DATE_FIN.isna()],
        ## Use commune code insee
        [df.COM,
         np.nan,
         np.nan,
         df.COM],
        ## Else use new commune code insee
        df.NEW_COM
    )

## Enriching df with commune name
df = (
    df
    .merge(
        geocode,
        on = ['COM','DATE_DEBUT','DATE_FIN'],
        how = 'left'
    )
)