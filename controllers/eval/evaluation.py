# 評価用データ作成プログラム
import pandas as pd
import numpy as np
from datetime import datetime as dt
import os
import matplotlib.pyplot as plt

out_file_path = 'out/result_2021_08_22_out/cmp/result5.csv'

def rename_columns(df):
    df_new_columns = ["時間"]
    setting_columns = []
    columns = []
    for i in df.columns:
        if "吸込温度" in i:
            df_new_columns.append(i+"_予測")
            columns.append(i)
        elif "設定温度" in i:
            setting_columns.append(i)

    return df_new_columns,columns,setting_columns

def create_graphes(df,columns,feature,floor,setting_columns):
    x = [i for i in range(len(df_merge))]
    fig = plt.figure(figsize=(20,20))

    ax_set_list = []

    y_base = 1.0
    for i in range(len(columns)):
        l_1 = columns[i]
        l_2 = l_1 + "_予測"
        l_3 = setting_columns[i]
        x_base = 0.05 if i % 2 == 0 else 0.55
        width = 0.4
        height = 0.12
        y_base -= 0.185 if i % 2 == 0 else 0
        ax_set = fig.add_axes([x_base,y_base,width,height])
        y1 = df[l_1].values
        y2 = df[l_2].values
        y3 = df[l_3].values
        ax_set_list.append([ax_set,(l_1,l_2,l_3),(x,y1,y2,y3)])

    for c,item in enumerate(ax_set_list):
        item[0].plot(item[2][0],item[2][1],label=item[1][0])
        item[0].plot(item[2][0],item[2][2],label=item[1][1])
        item[0].plot(item[2][0],item[2][3],label=item[1][2])
        item[0].legend(loc='upper left',fontsize=12)

        item[0].set_title("比較結果{}".format(c),fontsize=14)
        item[0].set_xlabel("時間[min]",fontsize=14)
        item[0].set_ylabel("温度[℃]",fontsize=14)
        item[0].set_ylim([18,30])

    plt.subplots_adjust(wspace=0.2, hspace=0.3)

    features_list = feature.split("_")[1:]
    dir_path = "eval/{0}-{1}-{2}/".format(features_list[0],features_list[1],features_list[2])
    os.makedirs(dir_path,exist_ok=True)
    output_file_path = "{0}{1}f_result{2}_{3}_{4}_{5}_{6}.png".format(dir_path,floor,dt.now().year,dt.now().month,dt.now().day,dt.now().hour,dt.now().minute)
    fig.savefig(output_file_path)


floor = out_file_path.split(".")[0][-1]

str_list = out_file_path.split("/")
features = str_list[1]

df_result = pd.read_csv(out_file_path,encoding="shift-jis")

time = df_result.iloc[0]["時間"]
dt_time = dt.strptime(time, '%Y-%m-%d %H:%M:%S')

base_dir = "data/evaluation/base/{0}_{1}_{2}/".format(dt_time.year,dt_time.month,dt_time.day)
base_file_path = base_dir + "all_bems_data{}.csv".format(floor)

df_base = pd.read_csv(base_file_path,encoding="shift-jis")
df_result.columns,extract_columns,setting_columns = rename_columns(df_base)
df_merge = pd.merge(df_base, df_result, on='時間', how="right")

create_graphes(df_merge,extract_columns,features,floor,setting_columns)