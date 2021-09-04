import datetime
import numpy as np
import matplotlib.pyplot as plt
import model
from ..cvt.conversion import dataset

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
     
model = model.HeatModel(20, 20, 5, 5, 30, dataset.control_data)

# for i in range(100):
#     model.step()

# agent_counts = np.zeros((model.grid.width, model.grid.height))
# for cell in model.grid.coord_iter():
#     cell_content, x, y, z = cell
#     if z == 2:
#         agent_temp = cell_content[0].temp
#         agent_counts[x][y] = agent_temp

# a = np.array(agent_counts).T[::-1]
# plt.imshow(a, interpolation='nearest')
# plt.tick_params(labelbottom=False,
#                labelleft=False,
#                labelright=False,
#                labeltop=False)
# plt.colorbar()
# plt.show()