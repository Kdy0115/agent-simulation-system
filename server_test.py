#!python3.5
import eel
import configparser
import subprocess
import threading
import sys
import os
import json
import glob
import time

import numpy as np
import seaborn as sns
from controllers import functions

global json_all_data

# ユーザー定義ファイル
# import main

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
    config_ini.read('config/config_test.ini', encoding='utf-8')

    config_ini["SIMULATION"]["start_time"] = start_time
    config_ini["SIMULATION"]["end_time"] = end_time
    config_ini["SIMULATION"]["output_folder_path"] = output_folder_path
    config_ini["BEMS"]["bems_file_path"] = bems_file_path
    config_ini["CONTROL"]["control_file_path"] = control_file_path
    config_ini["LAYOUT"]["heat_source_file_path"] = heat_source_file_path
    config_ini["LAYOUT"]["lyaout_floor_file_path"] = lyaout_floor_file_path
    config_ini["LAYOUT"]["skeleton_file_path"] = skeleton_file_path

    with open('config/config_test.ini', 'w',encoding="utf-8") as configfile:
        # 指定したconfigファイルを書き込み
        config_ini.write(configfile,True)
    
    
    
#################################################################################
# シミュレーション実行用サーバー側プログラム                                    #
#################################################################################    

@eel.expose
def start_simulation():
    print("シミュレーションを実行します")
    subprocess.run('py main.py', shell=True)

@eel.expose
def stop_simulation():
    print('シミュレーションを停止します')
    #subprocess.run()



@eel.expose
def prepare_simulation():
    thread1 = threading.Thread(target=simulation)
    thread1.start()
    

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
    json_open = open(path, 'r')
    json_all_data = json.load(json_open)


@eel.expose
def import_result_data(number):
    global json_all_data
    start = time.time()
    #print(path)
    
    data = json_all_data
    open_time = time.time()-start
    print("open_time = ",open_time)
    #print(data[number]["agent_list"][100]["temp"])
    data_x = []
    data_y = []
    data_z = []
    data_temp = []
    #need_data = []
    start1 = time.time()
    print(data)
    for i in range(len(data[number]["agent_list"])):
        if data[number]["agent_list"][i]["id"] > 10:
            data_x.append(data[number]["agent_list"][i]["x"])
            data_y.append(data[number]["agent_list"][i]["y"])
            data_z.append(data[number]["agent_list"][i]["z"])
            data_temp.append(data[number]["agent_list"][i]["temp"])
            #need_data.append(data[0]["agent_list"][i])

    sort_time = time.time()-start1
    print("sort_time = ",sort_time)
    return data_x,data_y,data_z,data_temp
        






    """
    json_open = open(path, 'r')
    data = json.load(json_open)
    all_data = []
    height_max = -1
    height_min = 10000
    width_max = -1
    width_min = 10000
    for i in data[0]["agent_list"]:
        if height_max < i["y"]:
            height_max = i["y"]
        if width_max < i["x"]:
            width_max = i["x"]
        if height_min > i["y"]:
            height_min = i["y"]
        if width_min > i["x"]:
            width_min = i["x"]

    for i in range(int(width_max)):
        for j in range(int(height_max)):
            for k in data[0]["agent_list"]:
                include_flag = False
                if "class" in k.keys():
                    if k["x"] == i and k["y"] == j and k["z"] == 1 and k["class"] == "space":
                        include_flag = True
                        all_data.append(k["temp"])
                        break
            if include_flag == False:
                all_data.append(-1)
    
    x_arr = []
    ac_id_arr = []
    result_arr = []
    for val in data[0]["agent_list"]:
        if "ac_id" in val.keys():
            id_dict = {
                "ac_id":val["ac_id"],
                "data":[]
            }
            ac_id_arr.append(val["ac_id"])
            result_arr.append(id_dict)
                

    
    result_data = {
        "max_height":height_max,
        "max_width" : width_max,
        "data"      : all_data
    }

    return result_data
    """

@eel.expose
def import_result_data_for_graph(path,x,y,z):
    global json_all_data
    
    data = json_all_data
    data_temp = []
    print(x)
    print(type(x))
    x = int(x)
    y = int(y)
    z = int(z)
    print(type(x))
    id = 0
    print(data[0]["agent_list"][11]["x"])
    print(type(data[0]["agent_list"][11]["x"]))
    if data[0]["agent_list"][11]["x"] == x:
        print("あってる")
    else:
        print("違う。")
    print(data[0]["agent_list"][11]["id"])
    for i in range(len(data[0]["agent_list"])):
        if data[0]["agent_list"][i]["x"] == x and data[0]["agent_list"][i]["y"] == y and data[0]["agent_list"][i]["z"] == z:
            id = data[0]["agent_list"][i]["id"]
            print("ok")
            #break

    print(id)

    for i in range(len(data[0]["agent_list"])):
        for k in range(len(data)):
            if data[k]["agent_list"][i]["id"] == id:
                data_temp.append(data[k]["agent_list"][i]["temp"])

    print(data_temp)

    return data_temp






@eel.expose
def print_heatmap(data):
    print("ヒートマップを出力します。")
    sns.heatmap(data)
    print("ヒートマップを出力出来ました？")

    np.random.seed(0)
    uniform_data = np.random.rand(10, 12)
    sns.heatmap(uniform_data)
    print("ヒートマップを出力出来ました？？")


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
    