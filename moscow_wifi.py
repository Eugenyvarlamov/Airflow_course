import requests
import pandas as pd
from pandas import json_normalize

api_key = 'b46c4c4987569ca542b55cf096cf7c27'
params = {'api_key': api_key}
datasets_ids = [60788, 60789, 60790]

def get_moscow_wifi(dataset_id):
    request_url = 'https://apidata.mos.ru/v1/features/{}'.format(dataset_id)
    r = (requests.post(request_url, json=['Address', 'NumberOfAccessPoints'], params=params)).json()
    return json_normalize(r['features'])

def all_moscow_wifi_points(datasets_ids):
    df = get_moscow_wifi(datasets_ids[0])
    for dataset_id in datasets_ids[1:]:
        df_temp = get_moscow_wifi(dataset_id)
        df = pd.concat([df, df_temp])
    return df.reset_index()

def addres_split(row):
    if ',' in row:
        return row.split(',')[1]
    
def cleaning(row):
    if 'город' in row or 'поселение' in row or 'поселок' in row:
        return 1
    else:
        return 2

try:
    df = all_moscow_wifi_points(datasets_ids)
except:
    print('Ошибка получения данных от сервера')
else:
    print('Данные получены, идет преобразование...')

print('Готово')

df['Street'] = df['properties.Attributes.Address'].apply(addres_split)
df_result = df.groupby('Street')['properties.Attributes.NumberOfAccessPoints'].sum().reset_index().sort_values(
    'properties.Attributes.NumberOfAccessPoints', ascending=False).head(10)

df_result['label'] = df_result['Street'].apply(cleaning)
df_result = df_result[df_result['label'] == 2]
df_result = df_result.rename({'Street': 'Улица', 'properties.Attributes.NumberOfAccessPoints':
                              'Кол-во точек'}, axis=1).reset_index()
df_result = df_result[['Улица', 'Кол-во точек']]
df_for_print = df_result.head(5)
df_for_print.index = [x for x in range(1,6)]
print('\n\n', df_for_print)
input('\n\nДля завершения нажмите любую клавишу')
