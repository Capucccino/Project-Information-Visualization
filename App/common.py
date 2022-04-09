import pandas as pd
import numpy as np
import math
from PIL import Image


# Import data
ssl = pd.read_csv('./Data/StaticSensorLocations.csv')
df = pd.read_csv('./Data/SSR_clean_avg.csv')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df3 = pd.read_csv('./Data/MSR_clean_avg.csv')
df3['Timestamp'] = pd.to_datetime(df3['Timestamp'])

# Create day and time range
hour_range = pd.date_range('2020-04-06 00:00:00',
                           '2020-04-10 23:59:45', freq='1h')
day_range = pd.date_range('2020-04-06 00:00:00',
                          '2020-04-11 23:59:45', freq='1D')

# Import map of St Himark
map_black = np.array(Image.open('./Images/test4.png'))
map_white = np.array(Image.open('./Images/test6.png'))

# usefull variable
available_mobile = np.sort(df3['Sensor-id'].unique())
available_line = np.sort(df['Sensor-id'].unique())

# Color used 
colors = ["#fd7f6f", "#7eb0d5", "#b2e061", "#bd7ebe", "#ffb55a", "#ffee65", "#beb9db", "#fdcce5", "#8bd3c7"]
radar_colors = ['rgb(253, 237, 176)', 'rgb(250, 205, 145)', 'rgb(246, 173, 119)', 'rgb(240, 142, 98)', 'rgb(231, 109, 84)', 'rgb(216, 80, 83)',
                  'rgb(195, 56, 90)', 'rgb(168, 40, 96)', 'rgb(138, 29, 99)', 'rgb(107, 24, 93)', 'rgb(76, 21, 80)', 'rgb(47, 15, 61)','rgb(0, 255, 73)']
font_colors = {
    'background': '#ede0d4',
    'background2':'#e6ccb2',
    'text': '#5e3023'}

# Return true if point (a,b) belongs to circle with center (x,y) 
def point_in_circle(a,b,x,y,radius):
    belong = False
    distance = math.sqrt((a-x)**2 + (b-y)**2)
    if radius - distance >= 0:
        belong = True
    return belong

# function to rescale a point according to the dimensions of the map
def resize(x, y):
    new_x = (x+120)/0.288249*774
    new_y = 619 - ((y)/0.238585*619)
    return new_x, new_y

# function to assign a color to a point according to its contamination value
def radar_color(value, max):
    if value > max:
        color = '#00ff49'
    else:
        index = int((value/max)*(len(radar_colors)-1))
        color = radar_colors[index]
    return color