import eel
import configparser
import subprocess
import threading
import sys
import os
import json
import glob
# ユーザー定義ファイル
# import main

eel.init('view',allowed_extensions=['.js','.html','.css'])

@eel.expose
def on_button_clicked():
    print("Button clicked[Python]")
    eel.showAlert("Button clicked!")

@eel.expose
def config_import():
    config_ini = configparser.ConfigParser()
    config_ini.read('config/config.ini', encoding='utf-8')

    config_bems       = config_ini["BEMS"]
    config_control    = config_ini["CONTROL"]
    config_simulation = config_ini["SIMULATION"]
    config_layout     = config_ini["LAYOUT"]
    config_calc       = config_ini["CALCULATION"]
    return config_simulation["Simulation_time"], config_simulation["Output_folder_path"], config_bems["BEMS_file_path"], config_control["Control_file_path"], config_layout["Heat_source_file_path"], config_layout["Lyaout_floor_file_path"], config_calc["multiprocess"]

@eel.expose
def configure_save(simulation_step,out_folder,bems_file,control_folder,source_folder,layout_folder,mp):
    config_ini = configparser.ConfigParser()
    config_ini.read('config/config.ini', encoding='utf-8')
    config_ini["SIMULATION"]["Simulation_time"] = simulation_step
    config_ini["SIMULATION"]["output_folder_path"] = out_folder
    config_ini["BEMS"]["bems_file_path"] = bems_file
    config_ini["CONTROL"]["control_file_path"] = control_folder
    config_ini["LAYOUT"]["heat_source_file_path"] = source_folder
    config_ini["LAYOUT"]["lyaout_floor_file_path"] = layout_folder
    if mp == "Yes":
        config_ini["CALCULATION"]["multiprocess"] = "True"
    else:
        config_ini["CALCULATION"]["multiprocess"] = "False"
    print("Save Configuration")
    with open('config/config.ini', 'w',encoding="utf-8") as configfile:
        # 指定したconfigファイルを書き込み
        config_ini.write(configfile,True)


def simulation():
    print("シミュレーションを実行します")
    subprocess.run('python main.py', shell=True)

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
def import_result_data(path):
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

@eel.expose
def exit_simulation():
    print("シミュレーションを中止します。")
eel.start('test/html/index.html',port=8080)
    