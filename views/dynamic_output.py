from mesa.visualization.ModularVisualization import ModularServer
from controllers.sml.model import *
from controllers.sml.extension.visualization.canvas_grid_visualization_extension import CanvasGrid_3d
from inc.common_function import format_color
from controllers.cvt.conversion import dataset

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

def output_web_api():
    grid = CanvasGrid_3d(agent_portrayal, 30, 30, 500, 500)
    server = ModularServer(HeatModel,
                           [grid],
                           "Heat Model",
                           {"width":25, "height":25, "depth":6, "floor":5, "simulation_step":30, "control_data":dataset.control_data})
    server.port = 8521 # The default
    server.launch()