from tokenize import group
import numpy
import pandas as pd
import matplotlib.pyplot as plt

def multiline_hourly_plot(dataset, avg = None, ycol = 'diff', ymin = None, ymax = None, opacity = None, title = None):
    fig, ax = plt.subplots()
    
    if ymin is not None:
        ax.set_ylim(bottom = ymin)
    
    if ymax is not None:
        ax.set_ylim(top = ymax)
        
    if opacity is None:
        opacity = 0.01

    for key,group in dataset:
        ax = group.groupby('hour').mean(numeric_only=True).plot(ax = ax, y = ycol, color = '#000000', alpha = opacity)
    
    if avg is not None:
        ax = avg.groupby('hour').mean(numeric_only=True).plot(ax = ax, y = ycol, color = '#FF0000', alpha = 1, linewidth = 2)
        
    if title is not None:
        ax.set_title(title)

    ax.legend().set_visible(False) # Disable the plot legend
    plt.show()

timeparser = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%s')

df = pd.read_csv('test_data.csv',delimiter=',',parse_dates = {'datetime': ['Time stamp']})
df.replace('unavailable', numpy.nan)
df.replace('unknown', numpy.nan)

df.fillna(method='ffill')
df['hour'] = df['datetime'].apply(lambda x: x.hour)
df['day'] = df['datetime'].apply(lambda x: x.timetuple().tm_yday)
df['diff'] = df['State'].diff().fillna(0)
df['weekday'] = df['datetime'].apply(lambda x: x.weekday() < 5)
df['max_energy'] = df['diff'].max()
df['norm_energy'] = df['diff'] / df['max_energy']
#df.groupby('hour').mean(numeric_only=True).plot(y='diff')
#df.groupby('hour').max(numeric_only=True).plot(y='diff')
#df.groupby('hour').min(numeric_only=True).plot(y='diff')
#plt.show()
multiline_hourly_plot(df[df.weekday == True].groupby('day'),opacity=0.5,ycol='norm_energy', avg=df[df.weekday == True])