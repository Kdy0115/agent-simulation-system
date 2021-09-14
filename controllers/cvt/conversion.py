import pandas as pd
import configparser
import os
import json
import csv
import datetime
import glob
from controllers.cvt.inc.cons import FLOOR5_COLUMN_NAME
# from inc.cons import FLOOR5_COLUMN_NAME

config_ini = configparser.ConfigParser()
config_ini.read('config/config.ini', encoding='utf-8')

config_bems       = config_ini["BEMS"]
config_control    = config_ini["CONTROL"]
config_simulation = config_ini["SIMULATION"]
config_layout     = config_ini["LAYOUT"]


class DataSet():
    def __init__(self, config_bems: str, config_control: str, config_layout: str, config_simulation: str,) -> None:

        self.bems_file_path = config_bems["BEMS_file_path"]
        
        self.control_data_folder_path = config_control["Control_file_path"]

        self.simulation_step = config_simulation["Simulation_time"]
        self.laytout_file_path = config_layout["Lyaout_floor_file_path"]
        self.output_folder = config_simulation["Output_folder_path"]
        
        self.floors = [3,4,5]
        self.init_bems_data = []
        self.control_data = []
        self.layout_data = []

    def create_output_folder(self) -> None:
        """ Create a folder for output file（結果出力ファイル用のフォルダを作成）
        """
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def import_all_control_data(self):
        files = glob.glob("{}*.csv".format(self.control_data_folder_path))
        for item,floor in zip(files,self.floors):
            control_data_dic = {}
            f = open(item,'r',encoding='shift-jis')
            data_list = []
            data = csv.DictReader(f)
            while True:
                try:
                    data_list.append(next(data))
                except StopIteration:
                    f.close()
                    break
            
            control_data_dic["floor"] = floor
            control_data_dic["control_data"]  = iter(data_list)

            self.control_data.append(control_data_dic)

    def import_all_layout_data(self):
        f = open(self.laytout_file_path)
        self.layout_data = json.load(f)
        f.close()
        


    def _import_bems_data(self) -> None:
        csv_file = open(self.bems_file_path, "r", encoding="shift-jis")
        f = csv.reader(csv_file)
        header = next(f)
        data = next(f)
        self.start_time = data[0]
        for floor in self.floors:
            init_bems_data = {}
            for key,value in zip(header,data):
                if key == "信号名称":
                    key = "時間"
                init_bems_data[key] = value
            init_bems_data["floor"] = floor
            self.init_bems_data.append(init_bems_data)

    def _sync_control_data(self) -> dict:
        
        tdatetime = datetime.datetime.strptime(self.start_time.replace("/","-"), '%Y-%m-%d %H:%M')
        start_time = tdatetime - datetime.timedelta(minutes=1)
        
        if start_time.hour < 10:
            hour = "0{}".format(start_time.hour)
        else:
            hour = str(start_time.hour)
        if start_time.minute < 10:
            minute = "0{}".format(start_time.minute)
        else:
            minute = str(start_time.minute)
        
        sync_time = "{0}:{1}".format(hour, minute)
        for control_data in self.control_data:
            while True:
                one_data_time = next(control_data["control_data"])
                if sync_time == one_data_time["時間"]:
                    break

    def integrate_files(self) -> None:
        self.post_data = {
            "simulation_step" :self.simulation_step,
            "simulation_data" :[],
            "output_folder"   :self.output_folder,
        }
        self._import_bems_data()
        self.import_all_control_data()
        self._sync_control_data()
        self.import_all_layout_data()

        for l in self.control_data:
            for m in self.layout_data:
                for n in self.init_bems_data:
                    if (l["floor"] == m["floor"]) and (m["floor"] == n["floor"]):
                        one_post_data = {
                            "init_bems_data": n,
                            "control_data"  : l["control_data"],
                            "layout_data"   : m
                        }
                    self.post_data["simulation_data"].append(one_post_data)

dataset = DataSet(config_bems, config_control, config_layout, config_simulation)
dataset.integrate_files()