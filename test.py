import pygsheets
import pandas as pd
import numpy as np

gc = pygsheets.authorize(service_file='clear-faculty-348813-1edaa94084f9.json')
sh = gc.open('Focus2')
#select the first sheet 
wks = sh[0]
data1 = wks.get_as_df()

#data1 = pd.read_csv("flatengagement_cal1.csv")

# time_start = 50
# data_array_1 = np.array(data1)

print(data1["Time"])