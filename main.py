import datetime
import numpy as np
import matplotlib.pyplot as plt
from controllers.sml.model import *
from controllers.cvt.conversion import dataset
import json
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
     
start = time.time()
model = HeatModel(25, 25, 6, 5, 30, dataset.control_data)
for i in range(300):
    model.step()
elapsed_time = time.time() - start
fw = open('test.json','w')
json.dump(model.spaces_agents_list,fw,indent=4)
print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

# agent_counts = np.zeros((model.grid.width, model.grid.height))
# print(model.grid._index_to_agent[0].pos)
# for agent in model.grid._index_to_agent.values():
#     if agent.pos[2] == 2 and agent.__class__.__name__ == "Space":
#         agent_temp = agent.temp
#         agent_counts[agent.pos[0]][agent.pos[1]] = agent_temp
# print(agent_counts)
# a = np.array(agent_counts).T[::-1]
# plt.imshow(a, interpolation='nearest')
# plt.tick_params(labelbottom=False,
#                labelleft=False,
#                labelright=False,
#                labeltop=False)
# plt.colorbar()
# plt.show()

# from mesa.visualization.modules import CanvasGrid
# from mesa.visualization.ModularVisualization import ModularServer


# def agent_portrayal(agent):
#     portrayal = {"Shape": "circle",
#                  "Filled": "true",
#                  "Layer": 0,
#                  "Color": "red",
#                  "r": 0.5}
#     return portrayal

# grid = CanvasGrid(agent_portrayal, 30, 30, 500, 500)
# server = ModularServer(HeatModel,
#                        [grid],
#                        "Heat Model",
#                        {"N":100, "width":30, "height":30})
# server.port = 8521 # The default
# server.launch()