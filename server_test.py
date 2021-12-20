from multiprocessing import process
import eel
import configparser
import subprocess
import threading
import sys
import os
import json
import glob

#import time
import pandas as pd
from datetime import datetime as dt


sys.path.append(os.getcwd())

# utils
from controllers import error,env,functions

import time
import subprocess

import numpy as np
import seaborn as sns
from controllers import functions
# from main import main

global json_all_data
# ユーザー定義ファイル
# import main

process_arr = []    
eel.init('view',allowed_extensions=['.js','.html','.css'])



@eel.expose
def test():
    print('接続済み')



@eel.expose
def on_button_clicked():
    print("Button clicked[Python]")
    eel.showAlert("Button clicked!")


#################################################################################
# 設定ファイルを編集用サーバー側プログラム                                      #
#################################################################################

@eel.expose
def config_import():
    """ 設定ファイルを読み込んでブラウザに返す関数

    Returns:
        config_simulation['start_time'] [date]          : シミュレーション開始時間
        config_simulation['end_time'] [date]            : シミュレーション終了時間
        config_bems['bems_file_path'] [str]             : BEMSファイルパス
        config_simulation['control_file_path'] [date]   : 制御計画ファイルパス
        
    """    
    config_ini = configparser.ConfigParser()
    config_ini.read('config/config.ini', encoding='utf-8')

    config_bems       = config_ini["BEMS"]
    config_control    = config_ini["CONTROL"]
    config_simulation = config_ini["SIMULATION"]
    config_layout     = config_ini["LAYOUT"]

    return config_simulation["start_time"], config_simulation['end_time'], config_bems['bems_file_path'], config_control['control_file_path'], config_layout['lyaout_floor_file_path'], config_layout['skeleton_file_path'], config_layout['heat_source_file_path'], config_simulation['output_folder_path']


@eel.expose
def configure_save(start_time,end_time,bems_file_path,control_file_path,lyaout_floor_file_path,skeleton_file_path,heat_source_file_path,output_folder_path):
    """ ブラウザから返された設定をconfig.iniに反映する関数

    Args:
        start_time ([type]): [description]
        end_time ([type]): [description]
        bems_file_path ([type]): [description]
        control_file_path ([type]): [description]
        lyaout_floor_file_path ([type]): [description]
        skeleton_file_path ([type]): [description]
        heat_source_file_path ([type]): [description]
        output_folder_path ([type]): [description]
    """    
    config_ini = configparser.ConfigParser()
    config_ini.read('config/config.ini', encoding='utf-8')
    
    if len(start_time) <= 16:
        start_time += ":00"
    if len(end_time) <= 16:
        end_time += ":00"
    config_ini["SIMULATION"]["start_time"] = start_time
    config_ini["SIMULATION"]["end_time"] = end_time
    config_ini["SIMULATION"]["output_folder_path"] = output_folder_path
    config_ini["BEMS"]["bems_file_path"] = bems_file_path
    config_ini["CONTROL"]["control_file_path"] = control_file_path
    config_ini["LAYOUT"]["heat_source_file_path"] = heat_source_file_path
    config_ini["LAYOUT"]["lyaout_floor_file_path"] = lyaout_floor_file_path
    config_ini["LAYOUT"]["skeleton_file_path"] = skeleton_file_path

    with open('config/config.ini', 'w',encoding="utf-8") as configfile:
        # 指定したconfigファイルを書き込み
        config_ini.write(configfile,True)
    
    
    
#################################################################################
# シミュレーション実行用サーバー側プログラム                                    #
#################################################################################

@eel.expose
def start_simulation():
    print("シミュレーションを実行します")
    cmd = "python main.py"      # シェル実行のコマンド
    p = subprocess.Popen(cmd)
    process_arr.append(p)
    
    # thread1 = threading.Thread(target=main)
    # thread1.start()

@eel.expose
def stop_simulation():
    for process in process_arr:
        process.kill()
    print('シミュレーションを停止しました')
        

@eel.expose
def prepare_simulation():
    thread1 = threading.Thread(target=simulation)
    thread1.start()
    
@eel.expose
def import_log_file():
    config_ini = configparser.ConfigParser()
    config_ini.read('config/config.ini', encoding='utf-8')
    file_path = config_ini["SIMULATION"]["output_folder_path"] + "log/progress.txt"
    f = open(file_path, 'r')
    data = (f.read()).split('\n')
    f.close()
    
    return int(data[-2])

@eel.expose
def render_dir():
    path = 'out'
    files = os.listdir(path)
    files_dir = [f for f in files if os.path.isdir(os.path.join(path, f))]

    return files_dir

@eel.expose
def render_floors(dir):
    path = 'out/{}/'.format(dir)
    files = os.listdir(path)
    floors = []
    for i in files:
        if '.json' in i:
            floors.append(i)
    return floors


@eel.expose
def open_json(path):
    print(path)
    global json_all_data
    path += 'result5.json'

    #path = 'out/test_result.json'

    json_open = open(path, 'r')
    json_all_data = json.load(json_open)


@eel.expose
def import_result_data(number):
    global json_all_data
    #start = time.time()
    #print(path)
    
    data = json_all_data
    #open_time = time.time()-start
    #print("open_time = ",open_time)
    #print(data[number]["agent_list"][100]["temp"])
    data_x = []
    data_y = []
    data_z = []
    data_temp = []
    #need_data = []
    start1 = time.time()
    for i in range(len(data[number]["agent_list"])):
        if data[number]["agent_list"][i]["class"] == "space":
            data_x.append(data[number]["agent_list"][i]["x"])
            data_y.append(data[number]["agent_list"][i]["y"])
            data_z.append(data[number]["agent_list"][i]["z"])
            data_temp.append(data[number]["agent_list"][i]["temp"])
            #need_data.append(data[0]["agent_list"][i])

    min_temp,max_temp = min(data_temp),max(data_temp)
    # sort_time = time.time()-start1
    # print("sort_time = ",sort_time)
    return data_x,data_y,data_z,data_temp,min_temp,max_temp

@eel.expose
def import_result_data_for_graph(path,x,y,z):
    global json_all_data
    
    data = json_all_data
    data_temp = []
    
    x,y,z = int(x),int(y),int(z)
    id = 0

    for i in range(len(data[0]["agent_list"])):
        if data[0]["agent_list"][i]["x"] == x and data[0]["agent_list"][i]["y"] == y and data[0]["agent_list"][i]["z"] == z:
            id = data[0]["agent_list"][i]["id"]


    for i in range(len(data[0]["agent_list"])):
        for k in range(len(data)):
            if data[k]["agent_list"][i]["id"] == id:
                data_temp.append(data[k]["agent_list"][i]["temp"])

    print(data_temp)

    return data_temp,max(data_temp)+0.1,min(data_temp)-0.1





@eel.expose
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


@eel.expose
def inhalation_temp_evaluation(out_file_path,base_file_path):
    """ 吸込温度側評価用関数

    Args:
        out_file_path [str] : シミュレーション結果ファイル（BEMS補完用）
        
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
    '''
    try:
        df_merge["外気温"] = df_base["外気温"].values
    except ValueError:
        df_merge["外気温"] = 0
    '''

    #output_dir += "inhalation/"
    
    df_merge["5f0温度差分"] = df_merge["5f0吸込温度"] - df_merge["5f0吸込温度_予測"]
    df_merge["5f2温度差分"] = df_merge["5f2吸込温度"] - df_merge["5f2吸込温度_予測"]
    
    extract_arr = []
    for i in df_merge.columns:
        if '温度差分' in i or '時間' in i:
            extract_arr.append(i)
            
    df_merge = df_merge[extract_arr]
    
    df_format = df_merge.to_dict()
    
    print(df_format)
    return df_format
    #return list(df_format['5f0温度差分'].values)
    #df_merge.to_csv(output_dir+"result.csv",encoding=env.glbal_set_encoding)
    

@eel.expose
def observe_temp_evaluation(observe_data,simulation_data,position_data):
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
    #dir_path = output_dir + "observe/"
    #os.makedirs(dir_path,exist_ok=True)
    #df_marge = dict(df_marge)
        
    #print(df_merge["596_予測値"])

    df_merge = df_merge.to_dict()
    print(df_merge)

    return df_merge
    #df_merge.to_csv(dir_path+"result.csv",encoding=env.glbal_set_encoding)
        

@eel.expose
def data_evaluation(out_file,observe_file,simulation_file,position,observe_flag,base_file_path):
    """ メイン関数

    Args:
        out_file [str]          : シミュレーション結果ファイル（BEMS補完用）
        observe_file [str]      : 評価用観測温度データのファイルパス（csv）
        simulation_file [str]   : シミュレーション結果ファイルパス（jsonのエージェントデータ）
        position [str]          : 温度取り位置座標データのファイルパス（json）
        observe_flag [bool]     : 温度取りデータで評価するかのフラグ
        output_dir [str]        : 出力先フォルダパス 使わなくなった
        base_file_path          : エアコンの吸い込み温度
    """    
    
    # 吸込温度側評価
    df_format = inhalation_temp_evaluation(out_file,base_file_path)
    # 温度取りデータ評価
    if observe_flag:
        evaluated_data=observe_temp_evaluation(observe_file,simulation_file,position)
        evaluated_data = dict(evaluated_data)
        print(df_format)
        print("--------------------------------------------")
        print(evaluated_data['596_予測値'])
        print(type(df_format))
        print(type(evaluated_data))
        return df_format,evaluated_data





#################################################################################
# レイアウト描画用サーバー側プログラム                                          #
#################################################################################

#################################################################################
# レイアウト描画用サーバー側プログラム                                          #
#################################################################################

@eel.expose
def import_layout_files(*args):
    """ レイアウト関連ファイルの読み込みを行いJSに返す関数

        args:
            args[0] [str]: レイアウトファイルパス
            args[1] [str]: 熱源情報ファイルパス
            args[2] [str]: 温度取り位置情報ファイルパス
            
        Returns:
            data_layout [dict]          : レイアウトデータ
            data_source [dict]          : 熱源情報データ
            data_observe_position [dict]: 温度取り位置情報データ
    """
    
    data_layout           = functions.import_json_file(args[0])
    data_source           = functions.import_json_file(args[1])
    data_position_observe = functions.import_json_file(args[2])
    
    return (data_layout,data_source,data_position_observe)

@eel.expose
def render_layout_dir():
    path = 'data/layout/'
    files = glob.glob("{}*".format(path))
    layout_files   = []
    source_files   = []
    position_files = []
    for file in files:
        file = file.replace('\\','/')
        if "floor" in file:
            layout_files.append(file)
        elif "source" in file:
            source_files.append(file)
        elif "position" in file:
            position_files.append(file)

    return [layout_files,source_files,position_files]
    


#################################################################################
# ヒートマップ編集（村上）                                                      #
#################################################################################
@eel.expose
def import_json_result_file(file_path):
    result_file = functions.import_json_file(file_path)
    
    return result_file

@eel.expose
def exit_simulation():
    print("シミュレーションを中止します。")


#################################################################################
# サーバー起動プログラム                                                        #
#################################################################################    

eel.start('index.html',port=8080)
    