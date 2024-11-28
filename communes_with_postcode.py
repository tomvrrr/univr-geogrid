from communes_core import *

## Loading Postal Code
postcode = (
    pd
    .read_csv('https://datanova.laposte.fr/data-fair/api/v1/datasets/laposte-hexasmal/metadata-attachments/base-officielle-codes-postaux.csv',
              dtype=str
    )
    .drop('ligne_5',axis = 1)
    .drop_duplicates()
    .rename(columns={
        'code_commune_insee':   'COM',
        '_geopoint':            'GPS_COORDINATES_2024',
        'code_postal':          'CODE_POSTAL_2024'
    })
    [['COM','CODE_POSTAL_2024','GPS_COORDINATES_2024']]
)

## Enriching df
df = df.merge(postcode,on = 'COM',how = 'left')