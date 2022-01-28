# Connect to google api and pull search trend data
import matplotlib.pyplot as plt
import pandas as pd
from pytrends.request import TrendReq

df_google_geos = pd.read_csv('google_trends_geos.csv')

if __name__ == '__main__':
    pytrends = TrendReq()
    list_keywords = ['inflation', 'monetary']
    pytrends.build_payload(list_keywords, timeframe='2017-01-01 2021-01-01', geo='US')
    df = pytrends.interest_over_time()
    plt.plot(df.index, df['inflation'])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
