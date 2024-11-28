# 🗺️ 🇫🇷 univr-geogrid 

A data pipeline for processing and compiling [INSEE](https://www.insee.fr/fr/information/2560452) source files related to french communes geographical attributes between 2020 and 2024.

## ⚙️ Building the table

To build the geogrid table, run `{shell} python save_geogrid.py`. This will create a `GEOGRID.csv` file using the ';' delimiter. 

### 📝 Description

The final table contains information derived from the source insee files during the 2020/2024 period and will contain:
- COM: The commune INSEE code, the most granular information available
- DATE_DEBUT/DATE_FUN: The period in which the commune exists
- NEW_COM: Derived from the [INSEE 2024](https://www.insee.fr/fr/information/7766585) commune event (*Évènements sur les communes*) if a commune changed commune INSEE code during the 2020/2024 period
- CODE_INSEE_XXXX: The valid code commune for a defined date. If the commune is allocated a new code, the year for which the change is effective will contain the newly allocated code (see NEW_COM) and the following year will be null
- TNCC/NCC/NCCENR/LIBELLE: The source commune information regarding name (see [INSEE 2024](https://www.insee.fr/fr/information/7766585) for reference)
- CODE_POSTAL: *Code postal* (valid in 2024) for a given commune (source [La Poste](https://datanova.laposte.fr/datasets/laposte-hexasmal))
- GPS_COORDINATES_2024: GPS Coordinate associated with the *Code postal*
- REG*, DEP*, CAN*, ARR*:  Region, Department, Canton and Arrondissement Source information from INSEE
- 2020,2021,2022,2023,2024: Validity of the REG*, DEP*, CAN*, ARR* information

### ⚠️ Data Limitations

Before aggregating, make sure
- Code Commune Duplication. Due to the evolving nature of communes (creation, fusion etc...), some communes might be duplicated. Look for duplicate in the 'COM' field. A good example are communes '01039' and '01138', which fused in 2023 and changed Canton Name in 2022
- Lyon / Paris / Marseille: Code Commune (COM) for the *arrondissements* are artificially derived from the [La Poste](https://datanova.laposte.fr/datasets/laposte-hexasmal) dataset (INSEE doesn't recognize *arrondissements* as distinct communes). Look for NCC field equals to 'LYON','MARSEILLE','PARIS'
- Some *Code postal* are duplicated (multiple COM codes per *Code postal*) as a consequence of Code Commune duplication, or simply because multiple communes shared the same *Code postal*

## Scripts escription

### Preparing the core table

- `communes_core.py`: Uses the list of all communes information and validity (2024) as the core table to start the pipeline
- `communes_with_postcode.py`: Enriches the core table with postal codes from 2024
- `enriching_communes.py`: Enriches the core table with all level geographical codes (department, region, canton, arrondissement)

### Preparing lookup data 

- `insee_millesime_links.py`: Links for the source insee files used to build the code lookup
- `insee_millesime_lookup.py`: Builds the code lookup

### Saving the file

- `save_geogrid.py`: Final processing before saving the file

## Other interesting links

- [French Cities] (https://tgrandje.github.io/french-cities/): A Python Package developed by [DREAL](https://www.hauts-de-france.developpement-durable.gouv.fr/)
- [Pynsee](https://github.com/InseeFrLab/pynsee): A python package to consume the [INSEE](https://www.insee.fr/fr/accueil) API
