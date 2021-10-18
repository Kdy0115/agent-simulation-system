import pandas as pd
import numpy as np
import configparser

config_ini = configparser.ConfigParser()
config_ini.read('config/config.ini', encoding='utf-8')

config_bems       = config_ini["BEMS"]
config_simulation = config_ini["SIMULATION"]


class EvaluationDataSet():

    def __init__(self, config_bems: str, config_simulation: str) -> None:
        self.bems_file_path = config_bems["BEMS_file_path"]
        self.output_folder = config_simulation["Output_folder_path"] + "cmp/result3.csv"

    def import_data(self):
        self.bems_data = pd.read_csv(self.bems_file_path,encoding="shift-jis")
        self.result_data = pd.read_csv(self.output_folder,encoding="shift-jis")
        result_data_columns = list(self.result_data.columns)
        for i in range(len(result_data_columns)):
            if "吸込温度" in result_data_columns[i]:
                result_data_columns[i] += "シミュレーション"
        self.result_data.columns = result_data_columns

    def __str__(self):
        return """評価用BEMSファイル：{0}\nシミュレーション結果ファイル：{1}""".format(self.output_folder,self.bems_file_path)

eval = EvaluationDataSet(config_bems, config_simulation)
eval.import_data()
print(eval.bems_data.head())
print(eval.result_data.head())
