import pandas as pd
import configparser
import os
import json
import csv
import datetime
import glob
from controllers.cvt.inc.cons import FLOOR5_COLUMN_NAME
import copy
# from inc.cons import FLOOR5_COLUMN_NAME

config_ini = configparser.ConfigParser()
config_ini.read('config/config.ini', encoding='utf-8')

config_bems       = config_ini["BEMS"]
config_control    = config_ini["CONTROL"]
config_simulation = config_ini["SIMULATION"]
config_layout     = config_ini["LAYOUT"]
config_mp         = config_ini["CALCULATION"]

# uni_code_set = "utf-8-sig"
uni_code_set = "shift-jis"

class DataSet():
    def __init__(self, config_bems: str, config_control: str, config_layout: str, config_simulation: str, mp: str) -> None:

        self.bems_file_path = config_bems["BEMS_file_path"]
        
        self.control_data_folder_path = config_control["Control_file_path"]

        self.simulation_step = config_simulation["Simulation_time"]
        self.laytout_file_path = config_layout["Lyaout_floor_file_path"]
        self.heat_source_file_path = config_layout["Heat_source_file_path"]
        self.output_folder = config_simulation["Output_folder_path"]

        self.mp_flag = True if mp["multiprocess"] == "True" else False
        
        # self.floors = [3,4,5]
        # self.floors = [3,4]
        self.floors = [5]
        
        self.init_bems_data = []
        self.control_data = []
        self.layout_data = []

        self.create_output_folder()

    def create_output_folder(self) -> None:
        """ Create a folder for output file（結果出力ファイル用のフォルダを作成）
        """
        dirs = self.output_folder + "cmp/"
        if not os.path.exists(dirs):
            os.makedirs(dirs)

    def import_all_control_data(self):
        files = glob.glob("{}*.csv".format(self.control_data_folder_path))
        for item,floor in zip(files,self.floors):
            control_data_dic = {}
            f = open(item,'r',encoding=uni_code_set)
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

    def import_heat_source_data(self):
        f = open(self.heat_source_file_path)
        self.source_data = json.load(f)
        f.close()

    def _import_bems_data(self) -> None:
        def _format_time(str_time):
            
            if len(str_time) == 19:
                str_time = str_time.replace("-","/")
                return str_time
            else:
                time_str = str_time.split()
                date_arr = time_str[0].split("/")
                year = date_arr[0]
                month = date_arr[1] if len(date_arr[1]) > 1 else "0"+date_arr[1]
                day = date_arr[2] if len(date_arr[2]) > 1 else "0"+date_arr[2]

                time_arr = time_str[1].split(":")
                hour = time_arr[0] if len(time_arr[0]) > 1 else "0"+time_arr[0]
                minutes = time_arr[1] if len(time_arr[1]) > 1 else "0"+time_arr[1]

                return "{0}/{1}/{2} {3}:{4}:00".format(year,month,day,hour,minutes)

        df = pd.read_csv(self.bems_file_path,encoding=uni_code_set)
        self.start_time = df["時間"][0]
        df_format = df[df.columns[df.columns != '時間']].astype("float")
        time_arr = []
        for i in df["時間"].values:
            time_arr.append(_format_time(i))
        df_format["時間"] = time_arr

        for floor in self.floors:
            init_bems_data = {}
            df_a_f = df_format.filter(regex='({}f|外気温|時間)'.format(floor),axis=1)
            dfs_dict_arr = []
            init_bems_data = {}
            for row in range(len(df_a_f)):
                dfs_dict_arr.append(dict(df_a_f.loc[row]))
            init_bems_data["floor"] = floor
            init_bems_data["bems_data"] = dfs_dict_arr
            self.init_bems_data.append(init_bems_data)

    def _sync_control_data(self) -> dict:
        
        # if "-" in self.start_time:
        # tdatetime = datetime.datetime.strptime(self.start_time.replace("/","-"),'%Y-%m-%d %H:%M')
        # start_time = tdatetime
        # sync_time = str(start_time)
        if "/" in self.start_time:
            sync_time = str(datetime.datetime.strptime(self.start_time.replace("/","-"),'%Y-%m-%d %H:%M'))
        else:
            sync_time = self.start_time
        # else:
        #     tdatetime = datetime.datetime.strptime(self.start_time.replace("/","-"), '%Y-%m-%d %H:%M')
        #     start_time = tdatetime
        #     if start_time.hour < 10:
        #         hour = "0{}".format(start_time.hour)
        #     else:
        #         hour = str(start_time.hour)

        #     if start_time.minute < 10:
        #         minute = "0{}".format(start_time.minute)
        #     else:
        #         minute = str(start_time.minute)
        
        #     sync_time = "{0}:{1}".format(hour, minute)
        
        for control_data in self.control_data:
            cnt = 0
            iter_control_data = copy.deepcopy(iter(control_data["control_data"]))
            while True:
                one_data_time = next(iter_control_data)
                cnt += 1
                if sync_time == one_data_time["時間"]:
                    break
            if cnt > 1:
                for i in range(cnt-1):
                    next(control_data["control_data"])

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
        self.import_heat_source_data()

        for l in self.control_data:
            for m in self.layout_data:
                for n in self.init_bems_data:
                    for o in self.source_data:
                        if (l["floor"] == m["floor"]) and (m["floor"] == n["floor"]) and (n["floor"] == o["floor"]):
                            one_post_data = {
                                "init_bems_data": n,
                                "control_data"  : l["control_data"],
                                "layout_data"   : m,
                                "source_data"   : o,
                            }
                            self.post_data["simulation_data"].append(one_post_data)

    def output_data(self,data):
        def _output_json(key,data):
            fw = open('{0}/result{1}.json'.format(self.output_folder,key),'w')
            json.dump(data,fw,indent=4)

        def _output_complement_data(key,data):
            # result_arr = sorted(data, key=lambda x: x['ac_id'])
            result_dic = {}
            columns = ["時間"]
            values = []
            for value in data:
                per_value = {}
                per_value["時間"] = value["timestamp"]
                for i in value["agent_list"]:
                    if "ac_id" in i:
                        if not i["ac_id"]+"吸込温度" in columns:
                            columns.append(i["ac_id"]+"吸込温度")
                        per_value[i["ac_id"]+"吸込温度"] = i["observe_temp"]
                values.append(per_value)

            with open('{0}cmp/result{1}.csv'.format(self.output_folder,key), 'w',encoding=uni_code_set,newline="") as csv_file:
                fieldnames = columns
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for row in values:
                    writer.writerow(row)
                
        for result in data:
            _output_json(result[0],result[1])
            _output_complement_data(result[0],result[1])

