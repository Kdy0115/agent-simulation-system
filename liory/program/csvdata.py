#!python3.5
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pypath = 'out/0705/result_3.csv'
pydf = pd.read_csv(pypath,engine='python',header=None,usecols=[2,3,4,5,6,7,8,9,10,11])
time = pd.read_csv(pypath,engine='python',header=None,usecols=[1])
#print(pydf)
#print(len(pydf))

artpath = 'artisoc/07-05/result.xlsx'
artdf = pd.read_excel(artpath,header=None,usecols=[4,5,6,7,8,9,10,11,12,13])
#print(artdf)
#print(len(artdf))

sourcepath = 'source/TREND_20210701_20210710.xlsx'
sourcedf = pd.read_excel(sourcepath,header=None,usecols=[83,84,85,86,87])

startday = 5
starthour = 0
period = 24
startpoint = 11+startday*1440+60*starthour


if len(pydf) > len(artdf):
    number_of_data = len(artdf)
else:
    number_of_data = len(pydf)

#print('データ数:',number_of_data-1)

if 60*period > number_of_data-1:
    print('データ数が不足しています。存在するデータ数の中で最小の物に合わせて出力します。')





#print(time)
timedata_0705 = []
pydata0_0705 = []
pydata1_0705 = []
pydata2_0705 = []
pydata3_0705 = []
pydata4_0705 = []
pydata5_0705 = []
pydata6_0705 = []
pydata7_0705 = []
pydata8_0705 = []
pydata9_0705 = []

for i in range(1,number_of_data):
    timedata_0705.append(time[1][i])
    pydata0_0705.append(pydf[2][i])
    pydata1_0705.append(pydf[3][i])
    pydata2_0705.append(pydf[4][i])
    pydata3_0705.append(pydf[5][i])
    pydata4_0705.append(pydf[6][i])
    pydata5_0705.append(pydf[7][i])
    pydata6_0705.append(pydf[8][i])
    pydata7_0705.append(pydf[9][i])
    pydata8_0705.append(pydf[10][i])
    pydata9_0705.append(pydf[11][i])

#print(len(pydata1_0705))


artdata0_0705 = []
artdata1_0705 = []
artdata2_0705 = []
artdata3_0705 = []
artdata4_0705 = []
artdata5_0705 = []
artdata6_0705 = []
artdata7_0705 = []
artdata8_0705 = []
artdata9_0705 = []

for i in range(1,number_of_data):
    artdata0_0705.append(artdf[4][i])
    artdata1_0705.append(artdf[5][i])
    artdata2_0705.append(artdf[6][i])
    artdata3_0705.append(artdf[7][i])
    artdata4_0705.append(artdf[8][i])
    artdata5_0705.append(artdf[9][i])
    artdata6_0705.append(artdf[10][i])
    artdata7_0705.append(artdf[11][i])
    artdata8_0705.append(artdf[12][i])
    artdata9_0705.append(artdf[13][i])

#print(artdata1_0705)


sourcedata1_0705 = []
sourcedata2_0705 = []
sourcedata3_0705 = []
sourcedata4_0705 = []
sourcedata5_0705 = []
for i in range(startpoint,startpoint+number_of_data):
    sourcedata1_0705.append(sourcedf[83][i])
    sourcedata2_0705.append(sourcedf[84][i])
    sourcedata3_0705.append(sourcedf[85][i])
    sourcedata4_0705.append(sourcedf[86][i])
    sourcedata5_0705.append(sourcedf[87][i])


def y1make(y1,art,py,source):
    y1.append(art)
    y1.append(py)
    y1.append(source)
    return y1

def y2make(y2,art,py,source):
    artgap = []
    for i in range(len(art)):
        gap = float(art[i])-float(source[i])
        artgap.append(gap)
    pygap = []
    for i in range(len(py)):
        gap = float(py[i])-float(source[i])
        pygap.append(gap)
    y2.append(artgap)
    y2.append(pygap)
    return y2


x = []
y1_0 = []
y1_1 = []
y1_2 = []
y1_3 = []
y1_4 = []
y1_5 = []
y1_6 = []
y1_7 = []
y1_8 = []
y1_9 = []
y2_0 = []
y2_1 = []
y2_2 = []
y2_3 = []
y2_4 = []
y2_5 = []
y2_6 = []
y2_7 = []
y2_8 = []
y2_9 = []

x = timedata_0705
y1_0 = y1make(y1_0,artdata0_0705,pydata0_0705,sourcedata1_0705)
y1_1 = y1make(y1_1,artdata1_0705,pydata1_0705,sourcedata1_0705)
y1_2 = y1make(y1_2,artdata2_0705,pydata2_0705,sourcedata2_0705)
y1_3 = y1make(y1_3,artdata3_0705,pydata3_0705,sourcedata2_0705)
y1_4 = y1make(y1_4,artdata4_0705,pydata4_0705,sourcedata3_0705)
y1_5 = y1make(y1_5,artdata5_0705,pydata5_0705,sourcedata3_0705)
y1_6 = y1make(y1_6,artdata6_0705,pydata6_0705,sourcedata4_0705)
y1_7 = y1make(y1_7,artdata7_0705,pydata7_0705,sourcedata4_0705)
y1_8 = y1make(y1_8,artdata8_0705,pydata8_0705,sourcedata4_0705)
y1_9 = y1make(y1_9,artdata9_0705,pydata9_0705,sourcedata5_0705)

y2_0 = y2make(y1_0,artdata0_0705,pydata0_0705,sourcedata1_0705)
y2_1 = y2make(y1_1,artdata1_0705,pydata1_0705,sourcedata1_0705)
y2_2 = y2make(y1_2,artdata2_0705,pydata2_0705,sourcedata2_0705)
y2_3 = y2make(y1_3,artdata3_0705,pydata3_0705,sourcedata2_0705)
y2_4 = y2make(y1_4,artdata4_0705,pydata4_0705,sourcedata3_0705)
y2_5 = y2make(y1_5,artdata5_0705,pydata5_0705,sourcedata3_0705)
y2_6 = y2make(y1_6,artdata6_0705,pydata6_0705,sourcedata4_0705)
y2_7 = y2make(y1_7,artdata7_0705,pydata7_0705,sourcedata4_0705)
y2_8 = y2make(y1_8,artdata8_0705,pydata8_0705,sourcedata4_0705)
y2_9 = y2make(y1_9,artdata9_0705,pydata9_0705,sourcedata5_0705)

# print(len(y1_1[0]),len(y1_1[1]),len(y1_1[2]))
# print(y1_1[1])
#print(y2_1)
x = [i for i in range(len(x))]
print(y1_0[0][0],y1_0[1][0],y1_0[2][0])
# print(x)

plt.plot(x,y1_1[0])
plt.plot(x,[float(i) for i in y1_1[1]])
plt.plot(x,[float(i) for i in y1_1[2][:-1]])
# plt.plot(x,y1_1[2][:-1])

plt.show()