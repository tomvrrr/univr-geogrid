import pandas as pd

## 
def dict_to_df_list(data: dict, cols: list) -> list:
    '''
    Create a list of dataframes with selected columns, normalized 
    as upper string and a new 'YEAR' column

    - data: the dictionnary formatted as {'YEAR':'PATH/URL_TO_DF'}
    - cols: the columns from the dataframe to be kept
    '''
    return [
        pd
        ## Read all columns as string
        .read_csv(d, dtype=str)
        ## Cleaning column names (upper string)
        .pipe(lambda d: d.set_axis(d.columns.str.upper(), axis=1))
        ## Retaining only columns of interests
        [cols]
        ## Deriving new column with year
        .assign(YEAR = y) 
        .drop_duplicates()
        for y, d in data.items()
    ]