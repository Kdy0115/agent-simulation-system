# python ライブラリ
import pandas as pd
import numpy as np
import copy
import datetime
import os


trend_data_file_path = 'data/src/TREND_76_6904050_20210814_20210827_20210828183418.xlsx'

df = pd.read_excel(trend_data_file_path,encoding="shift-jis")

all_data_dir_path = "data/config_data/base/"
control_data_dir_path = "data/config_data/control/"
init_bems_data_dir_path = "data/config_data/init_bems/"

# floors = [4,5]
floors = [5]

ac_arr = {
    4:["4f0","4f1","4f2","4f3","4f4","4f5","4f6","4f7","4f8","4f9"],
    5:["5f0","5f1","5f2","5f3","5f4","5f5","5f6","5f7","5f8","5f9"],
    6:["6f0","6f1","6f2","6f3","6f4","6f5","6f6","6f7","6f8","6f9"]
}


key_map_floor_dict = {
    4:{
        "時間":"信号名称",
        "4f0設定温度":"C4F 事務室中ペリ PACG_設定温度",
        "4f0運転モード":"C4F 事務室中ペリ PACG_運転モード",
#         "4f0風速":"C4F 事務室中ペリ PACG_風速",
        "4f0風速":"C4F 事務室中ペリ_風速",
        "4f0吸込温度":"C4F 事務室中ペリ PACG_吸込温度",
        "4f1設定温度":"C4F 事務室中ペリ PACG_設定温度",
        "4f1運転モード":"C4F 事務室中ペリ PACG_運転モード",
#         "4f1風速":"C4F 事務室中ペリ PACG_風速",
        "4f1風速":"C4F 事務室中ペリ_風速",
        "4f1吸込温度":"C4F 事務室中ペリ PACG_吸込温度",
        "4f2設定温度":"C4F 事務室中 PACG_設定温度",
        "4f2運転モード":"C4F 事務室中 PACG_運転モード",
        "4f2風速":"C4F 事務室中 PACG_風速",
        "4f2吸込温度":"C4F 事務室中 PACG_吸込温度",
        "4f3設定温度":"C4F 事務室中 PACG_設定温度",
        "4f3運転モード":"C4F 事務室中 PACG_運転モード",
        "4f3風速":"C4F 事務室中 PACG_風速",
        "4f3吸込温度":"C4F 事務室中 PACG_吸込温度",
        "4f4設定温度":"C4F 事務室南ペリ PACG_設定温度",
        "4f4運転モード":"C4F 事務室南ペリ PACG_運転モード",
        "4f4風速":"C4F 事務室南ペリ PACG_風速",
        "4f4吸込温度":"C4F 事務室南ペリ PACG_吸込温度",
        "4f5設定温度":"C4F 事務室南ペリ PACG_設定温度",
        "4f5運転モード":"C4F 事務室南ペリ PACG_運転モード",
        "4f5風速":"C4F 事務室南ペリ PACG_風速",
        "4f5吸込温度":"C4F 事務室南ペリ PACG_吸込温度",
        "4f6設定温度":"C4F 事務室南 PACG_設定温度",
        "4f6運転モード":"C4F 事務室南 PACG_運転モード",
        "4f6風速":"C4F 事務室南 PACG_風速",
        "4f6吸込温度":"C4F 事務室南 PACG_吸込温度",
        "4f7設定温度":"C4F 事務室南 PACG_設定温度",
        "4f7運転モード":"C4F 事務室南 PACG_運転モード",
        "4f7風速":"C4F 事務室南 PACG_風速",
        "4f7吸込温度":"C4F 事務室南 PACG_吸込温度",
        "4f8設定温度":"C4F 事務室南 PACG_設定温度",
        "4f8運転モード":"C4F 事務室南 PACG_運転モード",
        "4f8風速":"C4F 事務室南 PACG_風速",
        "4f8吸込温度":"C4F 事務室南 PACG_吸込温度",
        "4f9設定温度":"C4F 事務室東南 PAC_設定温度",
        "4f9運転モード":"C4F 事務室東南 PAC_運転モード",
        "4f9風速":"C4F 事務室東南 PAC_風速",
        "4f9吸込温度":"C4F 事務室東南 PAC_吸込温度",
        "外気温":"B館 RF 外気温度"
    },
5:{
        "時間":"信号名称",
        "5f0設定温度":"C5F 事務室中ペリ PACG_設定温度",
        "5f0運転モード":"C5F 事務室中ペリ PACG_運転モード",
        "5f0風速":"C5F 事務室中ペリ PACG_風速",
        "5f0吸込温度":"C5F 事務室中ペリ PACG_吸込温度",
        "5f1設定温度":"C5F 事務室中ペリ PACG_設定温度",
        "5f1運転モード":"C5F 事務室中ペリ PACG_運転モード",
        "5f1風速":"C5F 事務室中ペリ PACG_風速",
        "5f1吸込温度":"C5F 事務室中ペリ PACG_吸込温度",
        "5f2設定温度":"C5F 事務室中 PACG_設定温度",
        "5f2運転モード":"C5F 事務室中 PACG_運転モード",
        "5f2風速":"C5F 事務室中 PACG_風速",
        "5f2吸込温度":"C5F 事務室中 PACG_吸込温度",
        "5f3設定温度":"C5F 事務室中 PACG_設定温度",
        "5f3運転モード":"C5F 事務室中 PACG_運転モード",
        "5f3風速":"C5F 事務室中 PACG_風速",
        "5f3吸込温度":"C5F 事務室中 PACG_吸込温度",
        "5f4設定温度":"C5F 事務室南ペリ PACG_設定温度",
        "5f4運転モード":"C5F 事務室南ペリ PACG_運転モード",
        "5f4風速":"C5F 事務室南ペリ PACG_風速",
        "5f4吸込温度":"C5F 事務室南ペリ PACG_吸込温度",
        "5f5設定温度":"C5F 事務室南ペリ PACG_設定温度",
        "5f5運転モード":"C5F 事務室南ペリ PACG_運転モード",
        "5f5風速":"C5F 事務室南ペリ PACG_風速",
        "5f5吸込温度":"C5F 事務室南ペリ PACG_吸込温度",
        "5f6設定温度":"C5F 事務室南 PACG_設定温度",
        "5f6運転モード":"C5F 事務室南 PACG_運転モード",
        "5f6風速":"C5F 事務室南 PACG_風速",
        "5f6吸込温度":"C5F 事務室南 PACG_吸込温度",
        "5f7設定温度":"C5F 事務室南 PACG_設定温度",
        "5f7運転モード":"C5F 事務室南 PACG_運転モード",
        "5f7風速":"C5F 事務室南 PACG_風速",
        "5f7吸込温度":"C5F 事務室南 PACG_吸込温度",
        "5f8設定温度":"C5F 事務室南 PACG_設定温度",
        "5f8運転モード":"C5F 事務室南 PACG_運転モード",
        "5f8風速":"C5F 事務室南 PACG_風速",
        "5f8吸込温度":"C5F 事務室南 PACG_吸込温度",
        "5f9設定温度":"C5F 事務室東南 PAC_設定温度",
        "5f9運転モード":"C5F 事務室東南 PAC_運転モード",
        "5f9風速":"C5F 事務室東南 PAC_風速",
        "5f9吸込温度":"C5F 事務室東南 PAC_吸込温度",
        "5気温":"B館 RF 外気温度"
    },
6:{
        "時間":"信号名称",
        "6f0設定温度":"C6F 事務室中ぺリ PACG_設定温度",
        "6f0運転モード":"C6F 事務室中ペリ PACG_運転モード",
        "6f0風速":"C6F 事務室中ペリ PACG_風速",
        "6f0吸込温度":"C6F 事務室中ぺリ PACG_吸込温度",
        "6f1設定温度":"C6F 事務室中ぺリ PACG_設定温度",
        "6f1運転モード":"C6F 事務室中ペリ PACG_運転モード",
        "6f1風速":"C6F 事務室中ペリ PACG_風速",
        "6f1吸込温度":"C6F 事務室中ぺリ PACG_吸込温度",
        "6f2設定温度":"C6F 事務室中 PACG_設定温度",
        "6f2運転モード":"C6F 事務室中 PACG_運転モード",
        "6f2風速":"C6F 事務室中 PACG_風速",
        "6f2吸込温度":"C6F 事務室中 PACG_吸込温度",
        "6f3設定温度":"C6F 事務室中 PACG_設定温度",
        "6f3運転モード":"C6F 事務室中 PACG_運転モード",
        "6f3風速":"C6F 事務室中 PACG_風速",
        "6f3吸込温度":"C6F 事務室中 PACG_吸込温度",
        "6f4設定温度":"C6F 事務室南ペリ PACG_設定温度",
        "6f4運転モード":"C6F 事務室南ペリ PACG_運転モード",
        "6f4風速":"C6F 事務室南ペリ PACG_風速",
        "6f4吸込温度":"C6F 事務室南ペリ PACG_吸込温度",
        "6f5設定温度":"C6F 事務室南ペリ PACG_設定温度",
        "6f5運転モード":"C6F 事務室南ペリ PACG_運転モード",
        "6f5風速":"C6F 事務室南ペリ PACG_風速",
        "6f5吸込温度":"C6F 事務室南ペリ PACG_吸込温度",
        "6f6設定温度":"C6F 事務室南 PACG_設定温度",
        "6f6運転モード":"C6F 事務室南 PACG_運転モード",
        #"6f6風速":"C6F 事務室南 PACG_風速",
        "6f6吸込温度":"C6F 事務室南 PACG_吸込温度",
        "6f7設定温度":"C6F 事務室南 PACG_設定温度",
        "6f7運転モード":"C6F 事務室南 PACG_運転モード",
        #"6f7風速":"C6F 事務室南 PACG_風速",
        "6f7吸込温度":"C6F 事務室南 PACG_吸込温度",
        "6f8設定温度":"C6F 事務室南 PACG_設定温度",
        "6f8運転モード":"C6F 事務室南 PACG_運転モード",
        #"6f8風速":"C6F 事務室南 PACG_風速",
        "6f8吸込温度":"C6F 事務室南 PACG_吸込温度",
        "6f9設定温度":"C6F 事務室東南 PAC_設定温度",
        "6f9運転モード":"C6F 事務室東南 PAC_運転モード",
        "6f9風速":"C6F 事務室東南 PAC_風速",
        "6f9吸込温度":"C6F 事務室東南 PAC_吸込温度",
        "外気温":"B館 RF 外気温度"
    },
}


def init_cvt(df):
    df.columns = df.loc[6]
    df = df.drop(df.index[[0,1,2, 3,4, 5,6,7,8,9]])
    return df.loc[:,~df.columns.str.contains("ロスナイ|湿度|電力量|電流|ﾛｽﾅｲ")]

def split_floor_data(df,floor_arr):
    df = df.reset_index()
    start_time = df["信号名称"].loc[0]
    end_time   = df["信号名称"].loc[len(df)-1]
    df_floors = {}
    for floor in floor_arr:
        df_floors[floor] = df.loc[:,df.columns.str.contains("信号名称|外気温度|{}F".format(floor))]
    
    return df_floors, start_time, end_time

def select_columns(df):
    control_columns = []
    init_bems_columns = []
    for c in df.columns:
        if "吸込温度" in c:
            init_bems_columns.append(c)
        else:
            if("時間" in c) or ("外気温" in c):
                init_bems_columns.append(c)
                control_columns.append(c)
            else:
                control_columns.append(c)
    
    return init_bems_columns,control_columns


def adjustment_items(df_arr,season):
    df_result_dic = {}
    for floor,df in df_arr.items():
        air_con_area = [f'C{floor}F 事務室北ペリ PACG_',f'C{floor}F 事務室北 PACG_',f'C{floor}F 事務室中ペリ PACG_',f'C{floor}F 事務室中 PACG_',f'C{floor}F 事務室南ペリ PACG_',f'C{floor}F 事務室南 PACG_',f'C{floor}F 事務室東南 PAC_'] 
        df_result = copy.deepcopy(df)
        for one in air_con_area:
             # 運連状態が0なら電源OFF（0）
            df_result.loc[df_result[one+'運転']==0,one+'運転モード'] = 0
            # 運転状態が1で省エネレベルが2,3または運転モードが3なら送風（3）
            df_result.loc[(df_result[one+'運転']==1) & ((df_result[f'C館 {floor}F G50_省エネレベル'] == 2) | (df_result[f'C館 {floor}F G50_省エネレベル'] == 3) | (df_result[one+'運転モード'] == 3)),one+'運転モード'] = 3
             # 夏期の場合
            if season == 0:
                 # 運転状態が1で省エネレベルが1の場合は冷房（1）
                df_result.loc[(df_result[one+'運転']==1) & (df_result[f'C館 {floor}F G50_省エネレベル'] == 1),one+'運転モード'] = 1
            # 冬期の場合
            elif season == 1: 
                 # 運転状態が1で省エネレベルが1で運転モードが2のとき暖房（2）
                df_result.loc[(df_result[one+'運転']==1) & ((df_result[f'C館 {floor}F G50_省エネレベル'] == 1) & (df_result[one+'運転モード'] == 2)),one+'運転モード'] = 2
                 # 冬季のインペリ側
                if (one == f'C{floor}F 事務室中 PACG_') or (one == f'C{floor}F 事務室南 PACG_'):
                    # インペリ側で運転ONかつ暖房のときは＋４℃アップ制御 
                    df_result.loc[(df_result[one+'運転']==1) & (df_result[one+'運転モード'] == 2),one+'吸込温度'] += 4
            # 中間期の場合
            else:
                # 運転状態が1で省エネレベルが1の場合は冷房（1）
                df_result.loc[(df_result[one+'運転']==1) & (df_result[f'C館 {floor}F G50_省エネレベル'] == 1),one+'運転モード'] = 1
                # 運転状態が1で省エネレベルが1で運転モードが2のとき暖房（2）
                df_result.loc[(df_result[one+'運転']==1) & ((df_result[f'C館 {floor}F G50_省エネレベル'] == 1) & (df_result[one+'運転モード'] == 2)),one+'運転モード'] = 2
        
        df_result_dic[floor] = df_result
    return df_result_dic


def format_30min_span_data(df):
    index_arr = []
    for i in range(len(df)):
        if df.iloc[i]["時間"].minute == 0 or df.iloc[i]["時間"].minute == 30:
            index_arr.append(df.index[i])
    return df.loc[index_arr]

def select_columns(df):
    control_columns = []
    init_bems_columns = []
    for c in df.columns:
        if "吸込温度" in c:
            init_bems_columns.append(c)
        else:
            if("時間" in c) or ("外気温" in c):
                init_bems_columns.append(c)
                control_columns.append(c)
            else:
                control_columns.append(c)
    
    return init_bems_columns,control_columns

data_all = {}
for floor in floors:
    result_df = pd.DataFrame()
    data_all[floor] = result_df
    
df_cvt = init_cvt(df)
df_cvt_arr,start_time,end_time = split_floor_data(df_cvt,floors)

column = []
for i in df_cvt_arr[5].columns:
    if "設定温度" in i or "信号名称" in i:
        column.append(i)
        
result_df_dic = adjustment_items(df_cvt_arr,1)

for floor in floors:
    for key,value in key_map_floor_dict[floor].items():
        data_all[floor][key] = result_df_dic[floor][value].values
        
date_gap = (end_time - start_time).days

result_arr = []
for key,value in data_all.items():
    floors_data = {}
    floors_control_data = {}
    floors_init_bems_data = {}
    bems_columns, control_columns = select_columns(value)
    floors_data[key] = value
    floors_control_data[key] = value[control_columns]
    floors_init_bems_data[key] = value[bems_columns]
    result_arr.append(
        {
            "data":floors_data,
            "control":floors_control_data,
            "init_bems":floors_init_bems_data
        })

for i in result_arr:
    os.makedirs(all_data_dir_path,exist_ok=True)
    os.makedirs(control_data_dir_path,exist_ok=True)
    os.makedirs(init_bems_data_dir_path,exist_ok=True)
    for key in i["data"].keys():
        file_all_data_path = all_data_dir_path + "all_bems_data{}.csv".format(key)
        file_control_path  = control_data_dir_path + "control_{}.csv".format(key)
        file_init_bems_path  = init_bems_data_dir_path + "init_bems_{}.csv".format(key)

        i["data"][key].to_csv(file_all_data_path,encoding='shift-jis',index=False)
        i["control"][key].to_csv(file_control_path,encoding='shift-jis',index=False)
        i["init_bems"][key].to_csv(file_init_bems_path,encoding='shift-jis',index=False)