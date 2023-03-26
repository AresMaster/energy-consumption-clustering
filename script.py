import numpy
import pandas as pd
import matplotlib.pyplot as plt

timeparser = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%s')

df = pd.read_csv('test_data2.csv',delimiter=',',parse_dates = {'datetime': ['Time stamp']})
df = df.replace('unavailable', numpy.nan)
df.fillna(method='ffill')
df['hour'] = df['datetime'].apply(lambda x: x.hour)
df['diff'] = df['State'].diff().fillna(0)

df.groupby('hour').mean(numeric_only=True).plot(y='diff')
df.groupby('hour').max(numeric_only=True).plot(y='diff')
df.groupby('hour').min(numeric_only=True).plot(y='diff')
plt.show()