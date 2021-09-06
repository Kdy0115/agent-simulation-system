import pandas as pd
import configparser
import os
import csv

config_ini = configparser.ConfigParser()
config_ini.read('config/config.ini', encoding='utf-8')

bems_file_path = config_ini["DEFAULT"]["BEMS_file_path"]
control_file_path = config_ini["DEFAULT"]["Control_file_path"]
output_folder_path = config_ini["DEFAULT"]["Output_folder_path"]

class DataSet():
    def __init__(self, bems_data_path, control_data_path, output_folder):

        def _create_iterator_data(path):
            f = open(path,'r',encoding='shift_jis')
            return csv.DictReader(f)

        self.bems_data = _create_iterator_data(bems_data_path)
        self.control_data = _create_iterator_data(control_data_path)
        self.output_folder = output_folder

        self.create_output_folder()

    def create_output_folder(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

dataset = DataSet(bems_file_path, control_file_path, output_folder_path)