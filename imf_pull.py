# Pull data using the IMF API

import pandas as pd
import requests


def series_list(url):
    key = 'Dataflow'
    search_term = 'Trade'
    series_list = requests.get(f'{url}{key}').json()['Structure']['Dataflows']['Dataflow']

    for series in series_list:
        if search_term in series['Name']['#text']:
            print(f"{series['Name']['#text']}: {series['KeyFamilyRef']['KeyFamilyID']}")
            pass
        pass
    return


def find_dimensions(url, key):
    dimension_list = requests.get(f'{url}{key}').json()['Structure']['KeyFamilies']['KeyFamily']['Components']['Dimension']
    for n, dimension in enumerate(dimension_list):
        print(f"Dimension {n + 1}: {dimension['@codelist']}")
        pass
    return


def find_codes(url, key):
    dimension_list = requests.get(f'{url}{key}').json()['Structure']['KeyFamilies']['KeyFamily']['Components']['Dimension']
    key = f"CodeList/{dimension_list[2]['@codelist']}"
    code_list = requests.get(f'{url}{key}').json()['Structure']['CodeLists']['CodeList']['Code']
    for code in code_list:
        print(f"{code['Description']['#text']}: {code['@value']}")
        pass
    return


def pull_data(url, parameters):
    series = '.'.join([i[1] for i in param[1:4]])
    key = f'CompactData/{param[0][1]}/{series}{param[-1][1]}'
    r = requests.get(f'{url}{key}').json()

    # data portion of results
    data = r['CompactData']['DataSet']['Series']
    return data


new_url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
param = [('dataset', 'IFS'),
         ('freq', 'M'),
         # Brazil, Chile, Colombia
         ('country', 'BR+CL+CO'),
         ('series', 'PCPI_IX'),
         ('start', '?startPeriod=2020')]
query_data = pull_data(new_url, param)
# Create pandas dataframe, column = country, row = obs
df = pd.DataFrame({s['@REF_AREA']: # Each country/area
                   {i['@TIME_PERIOD']: float(i['@OBS_VALUE'])
                    for i in s['Obs']} for s in query_data})

# Convert index to datetime
df.index = pd.to_datetime(df.index)

# Calculate inflation rate and drop empty rows
df = (df.pct_change(12) * 100).round(1).dropna()


# new_key = 'DataStructure/DOT'
# find_dimensions(new_url, new_key)

print('done')

