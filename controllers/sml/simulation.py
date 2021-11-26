# -*- coding: utf-8 -*-

""" シミュレーション制御モジュール
"""



# python lib
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
import multiprocessing as mp

# utils
from controllers.sml.model import *
from controllers.sml.extension.visualization.canvas_grid_visualization_extension import CanvasGrid_3d
from controllers.sml.inc.define import *



class SimulationControl():
    """ シミュレーションの制御を行うクラス
    
        Attributes:
            simulation_step     [Int] : シミュレーション回数
            models_floor_dic    [dict]: フロア辞書
            dataset             [dict]: 辞書形式の結果データ
            output_folder       [str] : 出力先フォルダ名
    """    

    def __init__(self,post_data,dataclass):
        self.simulation_step = int(post_data["simulation_step"])
        self.models_floor_dic = {}
        self.dataset = post_data["simulation_data"]
        self.output_folder = post_data["output_folder"]
        self.dataclass = dataclass

        for data in self.dataset:
            model = HeatModel(data["init_bems_data"]["floor"], self.simulation_step, data["init_bems_data"], data["control_data"],data["layout_data"],data["source_data"])
            self.models_floor_dic[data["init_bems_data"]["floor"]] = model



    def _str_simulation_state(self):
        """ シミュレーション実行開始内容をコンソールに表示するモジュール
        """        
        
        print("Simulation starts")
        time.sleep(0.1)
        print("Simulation Calculation Steps: {}".format(self.simulation_step))
        time.sleep(0.1)
        print("Simulation Results Folder: {}".format(self.output_folder))
        
        

    # def output_agent_json(self):
    #     """
    #     """        
    #     for result in self.output_data:
    #         print('{0}/result{1}.json'.format(self.output_folder,result[0]))
    #         fw = open('{0}/result{1}.json'.format(self.output_folder,result[0]),'w')
    #         json.dump(result[1],fw,indent=4)
            
            

    def run_simulation(self,key,model,i):
        """ シミュレーション実行モジュール

        Args:
            key   [type]              : [description]
            model [エージェントモデル]: エージェントシミュレーションモデル
            i     [Int]               : ラベリングしたプロセス番号

        Returns:
            result [tupple]: 結果を格納したタプル
        """        
        
        # コンソールに出力する文字列
        info = f'プロセス#{i:>2} '
        for _ in tqdm(range(self.simulation_step), desc=info,position=i):
            if model.terminate:
                break
            else:
                model.step()

        result = (key,model.spaces_agents_list)
        return result
    
    

    def run_all_simulations(self):
        """ マルチプロセスなしの場合のシミュレーション制御モジュール

        Returns:
            result_arr [array]: シミュレーション実行結果を格納した配列
        """        
        
        start = time.time()
        self._str_simulation_state()
        result_arr = []
        for key,model in self.models_floor_dic.items():
            for i in tqdm(range(self.simulation_step+1)):
                if model.terminate:
                    break
                else:
                    model.step()
                    if (self.dataclass.bach == False) and (i%60 == 0):
                        self.dataclass.per_output_data(key,model.spaces_agents_list[-1],i)
            if self.dataclass.bach == True:
                result_arr.append((key,model.spaces_agents_list))
        elapsed_time = time.time() - start
        print("Simulation finished!")
        print("Simulation time:{}".format(int(elapsed_time)) + "[sec]")

        return result_arr
    
    

    def run_all_simulations_multi_process(self) -> dict:
        """ マルチプロセス時のシミュレーション制御モジュール

        Returns:
            output_data [dict]: マルチプロセスで辞書として保存した結果を返すモジュール
        """        
        
        # 現在の時間を取得
        start = time.time()
        # シミュレーション実行時のメッセージを出力
        self._str_simulation_state()
        # 関数の引数を定義
        args = list(zip(self.models_floor_dic.keys(),self.models_floor_dic.values(),range(3)))
        # 引数の長さ
        L = len(args)
        
        # マルチプロセスの実行
        with mp.Pool() as pool: 
            self.output_data = pool.starmap(self.run_simulation, args)
        print("\n" * L)
        
        # 実行時間の計算
        elapsed_time = time.time() - start
        print("Simulation finished!")
        print("Simulation time:{}".format(int(elapsed_time)) + "[sec]")

        return self.output_data