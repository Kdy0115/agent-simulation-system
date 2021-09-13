import pandas as pd
import configparser
import os
import csv
import glob
from inc.cons import *

config_ini = configparser.ConfigParser()
config_ini.read('config/config.ini', encoding='utf-8')

config_bems       = config_ini["BEMS"]
config_control    = config_ini["CONTROL"]
config_simulation = config_ini["SIMULATION"]
config_layout     = config_ini["LAYOUT"]


class DataSet():
    def __init__(self, config_bems: str, config_control: str, config_layout: str, config_simulation: str,) -> None:

        self.bems_data = {
            "file_path" : config_bems["BEMS_file_path"],
            "sheet_name": config_bems["Excel_sheet_name"],
        }
        
        self.control_data_folder_path = config_control["Control_file_path"]
        self.control_data = []

        self.simulation_step = config_simulation["Simulation_time"]
        self.output_folder = config_simulation["Output_folder_path"]
        
        self.floors = [3,4,5]

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


    def _format_bems_data(self) -> dict:
        df = pd.read_excel(self.bems_data["file_path"],sheet_name=self.bems_data["sheet_name"],header=7)
        df_recent_bems = df.tail(1)
        start_time = df_recent_bems["信号名称"].values[0]
        bems_dict_list = []
        for floor in self.floors:
            df_recent_bems = df_recent_bems.loc[:,df_recent_bems.columns.str.contains('信号名称|外気温|吸込温度')].rename(columns=FLOOR5_COLUMN_NAME)
            dict_bems = {key:value for key,value in zip(df_recent_bems.columns,df_recent_bems.iloc[0].values)}
            dict_bems["floor"] = floor
            bems_dict_list.append(dict_bems)

        return bems_dict_list,start_time

    def sync_control_data(self,start_time) -> dict:
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
            "simulation_data" :[]
        }
        bems_list,start_time = self._format_bems_data()
        self.import_all_control_data()
        self.sync_control_data(start_time)

        for item in self.control_data:
            for one in bems_list:
                if item["floor"] == one["floor"]:
                    one_floor_data = {
                        "init_bems": one,
                        "control_plan": item["control_data"],
                    }
                    self.post_data["simulation_data"].append(one_floor_data)

dataset = DataSet(config_bems, config_control, config_layout, config_simulation)
dataset.integrate_files()