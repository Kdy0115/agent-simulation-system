# BEMSのTrendデータを評価用にコンバート
import pandas as pd
import numpy as np
import datetime
import copy
import os
import inc.cons as cons

# df = pd.read_excel('source/TREND_20210701_20210710.xlsx')
df = pd.read_excel('data/src/TREND_76_6904050_20210701_20210807_20210808110542.xlsx')

floors = [4,5,6]

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
    
data_all = {}
for floor in floors:
    result_df = pd.DataFrame()
    data_all[floor] = result_df

df_cvt = init_cvt(df)
df_cvt_arr,start_time,end_time = split_floor_data(df_cvt,floors)

result_df_dic = adjustment_items(df_cvt_arr,0)

for floor in floors:
    for key,value in cons.key_map_floor_dict[floor].items():
        data_all[floor][key] = result_df_dic[floor][value].values

date_gap = (end_time - start_time).days

result_arr = []
base_time = start_time
for i in range(1,date_gap+1) :
    floors_data = {}
    floors_control_data = {}
    floors_init_bems_data = {}
    for key,value in data_all.items():
        next_time = base_time + datetime.timedelta(days=1)
        _value = value[(value["時間"] >= datetime.datetime(base_time.year,base_time.month,base_time.day))&(value["時間"] < datetime.datetime(next_time.year,next_time.month,next_time.day))]
        floors_data[key] = _value
        bems_columns, control_columns = select_columns(_value)
        floors_control_data[key] = _value[control_columns]
        floors_init_bems_data[key] = _value[bems_columns]
    result_arr.append(
        {
            "time":"{0}_{1}_{2}".format(base_time.year,base_time.month,base_time.day),
            "data":floors_data,
            "control":floors_control_data,
            "init_bems":floors_init_bems_data
        })
    base_time = next_time

for i in result_arr:
    time_dir = i["time"] + "/"
    os.makedirs(cons.all_data_dir_path + time_dir,exist_ok=True)
    os.makedirs(cons.control_data_dir_path + time_dir,exist_ok=True)
    os.makedirs(cons.init_bems_data_dir_path + time_dir,exist_ok=True)
    for key in i["data"].keys():
        file_all_data_path = cons.all_data_dir_path + time_dir + "all_bems_data{}.csv".format(key)
        file_control_path  = cons.control_data_dir_path + time_dir + "control_{}.csv".format(key)
        file_init_bems_path  = cons.init_bems_data_dir_path + time_dir + "init_bems_{}.csv".format(key)
        i["data"][key].to_csv(file_all_data_path,encoding='utf_8_sig')
        i["control"][key].to_csv(file_control_path,encoding='utf_8_sig')
        i["init_bems"][key].to_csv(file_init_bems_path,encoding='utf_8_sig')