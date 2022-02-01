# Economic data
# Pulls from some CSVs - this is messy and only temporary. Use APIs in the future

import pandas as pd


def read_imf_data():
    """
    :return: data frame with country-level inflation, gdp for 2020/2021
    """
    df_imf_stimulus = pd.read_csv('imf_oct_2021.csv').sort_values(by='Country')  # Load and sort alphabetically
    df_imf_stimulus.drop(df_imf_stimulus.columns.difference(['Country', 'GDP_above_subtotal', 'GDP_liq_subtotal']),
                         axis=1, inplace=True)  # drop unnecessary columns

    # Same for 2nd dataset
    df_world_bank_gdp = pd.read_csv('world_bank_gdp.csv').sort_values(by='Country Name')  # Load and sort alphabetically
    df_world_bank_gdp.drop(df_world_bank_gdp.columns.difference(['Country Name', '2020']), axis=1, inplace=True)

    # Same for 3rd dataset
    df_imf_inflation = pd.read_csv('imf_inflation.csv')
    df_imf_inflation.drop(df_imf_inflation.columns.difference(['Country', '2019', '2020', '2021']), axis=1, inplace=True)
    df_imf_inflation.rename(columns={'2019': 'inflation_2019',
                                            '2020': 'inflation_2020',
                                            '2021': 'inflation_2021'}, inplace=True)
    # Some columns came as strings, convert them to numeric
    numeric_cols = df_imf_inflation.columns.drop('Country')
    df_imf_inflation[numeric_cols] = df_imf_inflation[numeric_cols].apply(pd.to_numeric, errors='coerce')

    # Same for 4th dataset
    df_world_bank_CPI = pd.read_csv('world_bank_CPI.csv')
    df_world_bank_CPI = df_world_bank_CPI.merge(right=df_imf_inflation, how='inner', on='Country')
    df_world_bank_CPI['CPI_2021_estimated'] = df_world_bank_CPI['2020'] * ((df_world_bank_CPI['inflation_2021'] + 100) / 100)

    # Build new dataframe with important data compiled from the 4 sources. Merge them by country to concatenate together0
    df_econ_data = df_imf_stimulus.merge(df_world_bank_gdp, how='inner', left_on='Country', right_on='Country Name')
    df_econ_data.rename(columns={'2020': 'GDP_2020'}, inplace=True)
    df_econ_data = df_econ_data.merge(df_world_bank_CPI, how='inner', on='Country')
    df_econ_data.sort_values(by='GDP_2020', ascending=False, inplace=True)
    df_econ_data.dropna(axis=0, subset=['GDP_above_subtotal', 'GDP_2020'], inplace=True)
    # Calculate normalized inflation and stimulus as % of gdp
    df_econ_data['norm_inflation_2019'] = df_econ_data['CPI_2021_estimated'] / df_econ_data['2019']
    df_econ_data['norm_inflation_2020'] = df_econ_data['CPI_2021_estimated'] / df_econ_data['2020']
    df_econ_data['tot_stimulus'] = df_econ_data['GDP_above_subtotal'] + df_econ_data['GDP_liq_subtotal']
    df_econ_data.reset_index(inplace=True)

    # Discard unnecessary columns
    keep_cols = ['Country', 'tot_stimulus', 'GDP_2020', 'norm_inflation_2019', 'norm_inflation_2020']
    df_econ_data.drop(df_econ_data.columns.difference(keep_cols), axis=1, inplace=True)

    return df_econ_data


