# -*- coding: utf-8 -*-

""" シミュレーション結果評価ファイル
"""



# ライブラリ
import pandas as pd
from datetime import datetime as dt
import os
import json
import sys

sys.path.append(os.getcwd())

# utils
from controllers import error,env,functions


# 出力先フォルダパス
output_dir_path = "eval/result_2021_08_22/"

###################################################################
# 入力                                                            #
###################################################################
# シミュレーション結果フォルダ
out_simulation_result_dir = "out/result_2021_08_22/"
# 吸い込み評価用ファイルパス
base_file_inhalt_path = "data/config_data/2021_08_14_27/base/all_bems_data5.csv"

# 温度取りデータ評価用ファイル
observe_file_path = "data/config_data/observe/all/observe1.csv"
# 温度取りデータ位置座標ファイルパス
position_data = "data/layout/position.json"

###################################################################

# 読み込む吸い込み用シミュレーション結果ファイル
out_file_path = '{}cmp/result5.csv'.format(out_simulation_result_dir)
# 読み込む温度取り用シミュレーション結果ファイル
simulation_data = "{}/result5.json".format(out_simulation_result_dir)

# 温度取りデータ比較フラグ
observe_evaluation = True
# グラフ出力フラグ
graph_output       = True


# 同一日時の場合は現在の時間を設定する
now_time = dt.now()
output_dir_path += f"{now_time.year}_{now_time.month}_{now_time.day}_{now_time.hour}_{now_time.minute}/"


def rename_columns(df):
    """ 必要なカラムだけを抽出する関数

    Args:
        df [DataFrame]: 評価を行うDataFrame型のデータ

    Returns:
        df_new_columns  [array]: 出力用の新しいカラム
        columns         [array]: 元のデータのカラムで吸込温度のみ
        setting_columns [array]: 設定温度のカラム
    """    
    
    df_new_columns = ["時間"]
    setting_columns = []
    columns = []
    for i in df.columns:
        # 吸込温度のみを抽出
        if "吸込温度" in i:
            df_new_columns.append(i+"_予測")
            columns.append(i)
        # 設定温度のみを抽出
        elif "設定温度" in i:
            setting_columns.append(i)

    return df_new_columns,columns,setting_columns



def inhalation_temp_evaluation(out_file_path,output_dir,base_file_path):
    """ 吸込温度側評価用関数

    Args:
        out_file_path [str] : シミュレーション結果ファイル（BEMS補完用）
        output_dir [str]    : 出力先フォルダパス
    """
    
    floor = out_file_path.split(".")[0][-1]

    df_result = pd.read_csv(out_file_path,encoding="shift-jis")

    time = df_result.iloc[0]["時間"]
    dt_time = dt.strptime(time, '%Y-%m-%d %H:%M:%S')

    # base_dir = "data/evaluation/base/{0}_{1}_{2}/".format(dt_time.year,dt_time.month,dt_time.day)
    # base_dir = "data/sample_data2/base/"
    base_file_path = base_file_path

    df_base = pd.read_csv(base_file_path,encoding="shift-jis")
    df_result.columns,extract_columns,setting_columns = rename_columns(df_base)
    df_merge = pd.merge(df_base, df_result, on='時間', how="right")
    try:
        df_merge["外気温"] = df_base["外気温"].values
    except ValueError:
        df_merge["外気温"] = 0

    output_dir += "inhalation/"
    
    df_merge["5f0温度差分"] = df_merge["5f0吸込温度"] - df_merge["5f0吸込温度_予測"]
    df_merge["5f2温度差分"] = df_merge["5f2吸込温度"] - df_merge["5f2吸込温度_予測"]
    
    extract_arr = []
    for i in df_merge.columns:
        if '温度差分' in i or '時間' in i:
            extract_arr.append(i)
            
    df_merge = df_merge[extract_arr]
    
    df_format = dict(df_merge)
    print(df_format)
    exit()
    #df_merge.to_csv(output_dir+"result.csv",encoding=env.glbal_set_encoding)
    

def observe_temp_evaluation(observe_data,simulation_data,position_data,output_dir):
    """ 温度取り評価用関数

    Args:
        observe_data [str]      : 評価用観測温度データのファイルパス（csv）
        simulation_data [str]   : シミュレーション結果ファイルパス（jsonのエージェントデータ）
        position_data [str]     : 温度取り位置座標データのファイルパス（json）
        output_dir [str]        : 出力先フォルダパス
    """    
    df_observe = pd.read_csv(observe_data,encoding="shift-jis")
    json_open = open(simulation_data, 'r')
    json_load = json.load(json_open)

    json_position = open(position_data, 'r')
    json_load_position = json.load(json_position)
    
    find_id_arr = json_load[0]["agent_list"]
    
    # 温度取りの座標と一致する空間を取得
    observe_space_id_arr = []
    for i in json_load_position:
        sensor_id,x,y,z = i["id"],i["x"],i["y"],i["z"]
        for agent in find_id_arr:
            if agent["class"] == "space":
                if (agent["x"] == x) and (agent["y"] == y) and (agent["z"] == z):
                    observe_space_id_arr.append((sensor_id,agent["id"]))
                    
                    
    columns = [str(i[0])+"_予測値" for i in observe_space_id_arr]
    columns.append("時間")
    result_df = pd.DataFrame(data=[],columns=columns)
    
    base_columns = list(result_df.columns)
    for per_time_data in json_load:
        time = per_time_data["timestamp"]
        row = [0] * len(base_columns)
        for agent in per_time_data["agent_list"]:
            for space in observe_space_id_arr:
                if agent["id"] == space[1]:
                    row[base_columns.index("{}_予測値".format(space[0]))] = agent["temp"]
        row[-1] = time
        result_df.loc[len(result_df)] = row
        
    df_merge = pd.merge(result_df,df_observe,on="時間",how="left")
    dir_path = output_dir + "observe/"
    #os.makedirs(dir_path,exist_ok=True)
    print(df_merge["596_予測値"])
        
    #df_merge.to_csv(dir_path+"result.csv",encoding=env.glbal_set_encoding)
        


def main(out_file,observe_file,simulation_file,position,observe_flag,output_dir,base_file_path):
    """ メイン関数

    Args:
        out_file [str]          : シミュレーション結果ファイル（BEMS補完用）
        observe_file [str]      : 評価用観測温度データのファイルパス（csv）
        simulation_file [str]   : シミュレーション結果ファイルパス（jsonのエージェントデータ）
        position [str]          : 温度取り位置座標データのファイルパス（json）
        observe_flag [bool]     : 温度取りデータで評価するかのフラグ
        output_dir [str]        : 出力先フォルダパス
    """    
    # 吸込温度側評価
    inhalation_temp_evaluation(out_file,output_dir,base_file_path)
    # 温度取りデータ評価
    if observe_flag:
        observe_temp_evaluation(observe_file,simulation_file,position,output_dir)



<<<<<<< HEAD
main(out_file_path,observe_file_path,simulation_data,position_data,observe_evaluation,output_dir_path,base_file_path)
=======
main(out_file_path,observe_file_path,simulation_data,position_data,observe_evaluation,output_dir_path,base_file_inhalt_path)
>>>>>>> 15f88fd5dbd65edfcb00e9c7da4909e32a7b4193
