#!python3.5
import pandas as pd
'''
sourcepath = 'data/source/TREND_20210701_20210710.xlsx'
sourcedf = pd.read_excel(sourcepath,header=None,usecols=[83,84,85,86,87])
#print(sourcedf)
#print(len(sourcedf))
day = 5
startpoint = 11+day*1440
sourcedata1_0705 = []
sourcedata2_0705 = []
sourcedata3_0705 = []
sourcedata4_0705 = []
sourcedata5_0705 = []
for i in range(startpoint,startpoint+1440):
    sourcedata1_0705.append(sourcedf[83][i])
    sourcedata2_0705.append(sourcedf[84][i])
    sourcedata3_0705.append(sourcedf[85][i])
    sourcedata4_0705.append(sourcedf[86][i])
    sourcedata5_0705.append(sourcedf[87][i])

#print(sourcedata1_0705)
'''
pypath = 'data/out/0705/result_3.csv'
pydf = pd.read_csv(pypath,engine='python',header=None,usecols=[2,3,4,5,6,7,8,9,10])
#print(pydf)

time = pd.read_csv(pypath,engine='python',header=None,usecols=[1])
#print(time)

timedata_0705 = []
pydata1_0705 = []
pydata2_0705 = []
pydata3_0705 = []
pydata4_0705 = []
pydata5_0705 = []
pydata6_0705 = []
pydata7_0705 = []
pydata8_0705 = []
pydata9_0705 = []
for i in range(1,1440):
    timedata_0705.append(time[1][i])
    pydata1_0705.append(pydf[2][i])
    pydata2_0705.append(pydf[3][i])
    pydata3_0705.append(pydf[4][i])
    pydata4_0705.append(pydf[5][i])
    pydata5_0705.append(pydf[6][i])
    pydata6_0705.append(pydf[7][i])
    pydata7_0705.append(pydf[8][i])
    pydata8_0705.append(pydf[9][i])
    pydata9_0705.append(pydf[10][i])

#print(timedata_0705)

'''
artpath = 'data/artisoc/07-05/result.xlsx'
artdf = pd.read_excel(artpath,header=None,usecols=[4,5,6,7,8,9,10,11,12,13])
#print(artdf)

artdata1_0705 = []
artdata2_0705 = []
artdata3_0705 = []
artdata4_0705 = []
artdata5_0705 = []
artdata6_0705 = []
artdata7_0705 = []
artdata8_0705 = []
artdata9_0705 = []
for i in range(1,1440):
    artdata1_0705.append(artdf[4][i])
    artdata2_0705.append(artdf[5][i])
    artdata3_0705.append(artdf[6][i])
    artdata4_0705.append(artdf[7][i])
    artdata5_0705.append(artdf[8][i])
    artdata6_0705.append(artdf[9][i])
    artdata7_0705.append(artdf[10][i])
    artdata8_0705.append(artdf[11][i])
    artdata9_0705.append(artdf[12][i])
'''