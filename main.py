# -*- coding: utf-8 -*-

""" シミュレーション実行モジュール

Todo:
    * /Thermal Agent Simulation/config/config.iniにシミュレーション設定ファイルを記載しないと実行されない
"""

# ライブラリ
from controllers.sml.simulation import SimulationControl
from controllers.cvt.conversion import *
import time
import configparser
import multiprocessing as mp

# 設定ファイルの内容を取得
config_ini = configparser.ConfigParser()
config_ini.read('config/config.ini', encoding='utf-8')

config_bems       = config_ini["BEMS"]
config_control    = config_ini["CONTROL"]
config_simulation = config_ini["SIMULATION"]
config_layout     = config_ini["LAYOUT"]
config_mp         = config_ini["CALCULATION"]

# pandasで扱うデータの文字コードの指定
# uni_code_set = "utf-8-sig"
uni_code_set = "shift-jis"



# DataSetクラスからインスタンスの生成(cvt内のファイルから参照)
dataset = DataSet(config_bems, config_control, config_layout, config_simulation, config_mp,uni_code_set)
# 必要ファイルのデータ統合
simulation_setting_data = dataset.integrate_files()

# SimulationControlからインスタンスの生成
simulation = SimulationControl(simulation_setting_data)

# マルチプロセス処理がTrueの場合
if dataset.mp_flag:
    if __name__ == '__main__':
        mp.freeze_support()
        # シミュレーションをマルチプロセス処理
        result = simulation.run_all_simulations_multi_process()
        # 計算結果をJsonファイルで出力
        dataset.output_data(result)
# マルチプロセス処理がFalseの場合
else:
    # シミュレーションを単一プロセスで処理
    result = simulation.run_all_simulations()
    dataset.output_data(result)
