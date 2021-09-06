import datetime
import numpy as np
import matplotlib.pyplot as plt
from controllers.sml.model import *
from controllers.cvt.conversion import dataset
from controllers.sml.extension.visualization.canvas_grid_visualization_extension import CanvasGrid_3d
from mesa.visualization.ModularVisualization import ModularServer
import json
import math
import time

source_data = [
    {
        "x":1,
        "y":2,
        "z":2,
        "size":1,
        "kind":2
    }
]

# class Simulation():
#     """ Simulation execusion class （シミュレーション実行クラス）
#     """
#     def __init__(self,data):
#         def set_simulation_space(bems_data,source_data):
#             """ Set simulation space from heat source information（熱源情報からシミュレーション空間を設定）
#             """

            
#         self.floor = data["floor"]
#         self.bems_data = data["bems_data"]
#         self.control_data = data["control_data"]
#         self.source_data = data["source_data"]
#         self.date = data["start_date"]
     
# start = time.time()
# model = HeatModel(25, 25, 6, 5, 30, dataset.control_data)
# for i in range(60):
#     model.step()
# elapsed_time = time.time() - start
# fw = open('test.json','w')
# json.dump(model.spaces_agents_list,fw,indent=4)
# print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

# from mesa.visualization.modules import CanvasGrid



def ColorScaleBCGYR(in_value):
    # 0.0～1.0 の範囲の値をサーモグラフィみたいな色にする
    # 0.0                    1.0
    # 青    水    緑    黄    赤
    # 最小値以下 = 青
    # 最大値以上 = 赤
    ret = 0
     #alpha値
    a = 255
    #RGB値
    r, g, b = 0, 0, 0 
    value = in_value
    tmp_val = math.cos( 4 * math.pi * value )
    col_val = (int)( ( -tmp_val / 2 + 0.5 ) * 255 )
    # 赤
    if value >= 4.0 / 4.0:
        r = 255
        g = 0      
        b = 0 
    # 黄～赤
    elif value >= 3.0 / 4.0 :
        r = 255     
        g = col_val 
        b = 0
     # 緑～黄
    elif value >=  2.0 / 4.0:
        r = col_val
        g = 255     
        b = 0         
    # 水～緑
    elif value >=  1.0 / 4.0:
        r = 0       
        g = 255     
        b = col_val    
    # 青～水
    elif value >=  0.0 / 4.0:
        r = 0       
        g = col_val 
        b = 255
    # 青
    else:                               
        r = 0       
        g = 0       
        b = 255    
    ret = (r,g,b)

    color_code = '#%02x%02x%02x' % ret
    return color_code

def format_color(value):
    min_temp = 18
    max_temp = 25
    return ColorScaleBCGYR((value-min_temp)/(max_temp-min_temp))

def agent_portrayal(agent):
    if agent.__class__.__name__ == "HeatSource":
        color = "green"
    else:
        color = format_color(agent.temp)

    portrayal = {"Shape": "rect",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": color,
                 #"r": 0.5
                 "h": 1,
                 "w": 1,
    }
    return portrayal

grid = CanvasGrid_3d(agent_portrayal, 30, 30, 500, 500)
server = ModularServer(HeatModel,
                       [grid],
                       "Heat Model",
                       {"width":25, "height":25, "depth":6, "floor":5, "simulation_step":30, "control_data":dataset.control_data})
server.port = 8521 # The default
server.launch()