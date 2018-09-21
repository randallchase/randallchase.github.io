import pandas as pd
from ast import literal_eval


def col_to_dtg(df, label):
    df[label] = pd.to_datetime(df[label])
    return df


iter_csv = pd.read_csv('PS02/Crime_Data_from_2010_to_Present.csv',
                       iterator=True, chunksize=1000)

la_crime = pd.concat([col_to_dtg(chunk, 'Date Occurred') for chunk in iter_csv])

dtg_mask = (la_crime['Date Occurred'] >= '2017-1-1') &\
       (la_crime['Date Occurred'] <= '2017-12-31')
la_crime = la_crime[dtg_mask]

areas = ['Central']
local_crime = la_crime[la_crime['Area Name'].isin(areas)].copy()
local_crime = local_crime.dropna(subset=['Location '])
local_crime['Location '] = local_crime['Location '].apply(literal_eval)

local_crime = local_crime.reset_index(drop=True)
local_crime.to_json('./PS02/la_crime.json', orient='split', index=False)
