# Connect to google api and pull search trend data
# Working file, to be updated in the future (not in use yet)

import matplotlib.pyplot as plt
import pandas as pd
from economic_data import read_imf_data
from pytrends.request import TrendReq

df_google_geos = pd.read_csv('google_trends_geos.csv')  # Load all geographic tags/labels for use in Google Trends API
df_economic = read_imf_data()  # Pull Economic Data from csvs
series_countries = df_economic['Country']  # Select Countries to plot on right-hand side (inflation vs. stimulus)
dict_country_ids = {    # Using this dictionary to choose countries to put into google API
    'AU': 'Australia',
    'CA': 'Canada',
    'DE': 'Germany',
    'FR': 'France',
    'GB': 'United Kingdom',
    'ID': 'Indonesia',
    'IN': 'India',
    'IT': 'Italy',
    'SE': 'Sweden',
    'TR': 'Turkey',
    'US': 'United States',
}
num_countries = len(dict_country_ids)

# First plot on right hand side = inflation vs. stimulus
fig = plt.figure()
gs0 = fig.add_gridspec(1, 2)  # split into 2 vertical sections
gs1 = gs0[0].subgridspec(num_countries, 1)  # split LH side into the number of countries that will be plotted
ax = fig.add_subplot(gs0[1])  # Add right-hand subplot (infl x stim)
x_data = df_economic['tot_stimulus']  # select data to plot
y_data = df_economic['norm_inflation_2020'] * 100
dot_sizes = 1E-10 * df_economic['GDP_2020']
ax.scatter(x_data, y_data, s=dot_sizes, label='Marker Size = 2020 GDP')  # scatter plot with gdp size as marker size
plt.legend(loc='best')  # Is OK but would like to be able to select the size of the marker legend

label_countries = df_economic['Country'][0:12]  # Too busy if you mark every one, so take largest # economies
for i, country in enumerate(label_countries):
    ax.annotate(country, (x_data[i], y_data[i]))  # and label them/
    pass
ax.legend()
ax.set_ylim([98, 110])
ax.set_xlabel('Total Stimulus (% of GDP)')
ax.set_ylabel('Normalized Price Index, YE-2021 (YE-2020=100)')

# Now, compile the google trends data
pytrends = TrendReq()
list_keywords = ['inflation', 'monetary']

for idx, country_id in enumerate(dict_country_ids):  # Loop through each country
    pytrends.build_payload(list_keywords, timeframe='2020-01-01 2022-01-01', geo=country_id)  # Build payload
    df = pytrends.interest_over_time()  # Get the time-series data for this country

    # Had some missing data, so sets plot data only if that column has values. Otherwise, sets to empty
    if 'inflation' in df:
        y_vals = df.inflation
    else:
        y_vals = []
        pass
    # Add subplot for each country timeseries
    ax = fig.add_subplot(gs1[idx])
    ax.plot(df.index, y_vals, label=dict_country_ids.get(country_id))
    ax.legend(loc='upper left')

    # Add title for first plot (on top)
    if idx == 0:
        ax.set_title('Relative frequency of "inflation" in Google searches')
        pass

    # Remove x-ticks for middle plots to save clutter
    if idx < num_countries - 1:
        ax.set_xticklabels("")
        pass
    pass

plt.show()
