import datetime
import numpy as np
import matplotlib.pyplot as plt
from controllers.sml.model import *
from controllers.cvt.conversion import dataset
from controllers.sml.extension.visualization.canvas_grid_visualization_extension import CanvasGrid_3d
from tqdm import tqdm
import json
import math
import time
from multiprocessing import Process
import multiprocessing

class SimulationControl():

    def __init__(self,post_data):
        self.simulation_step = int(post_data["simulation_step"]) * 60
        self.models_floor_dic = {}
        self.dataset = post_data["simulation_data"]
        self.output_folder = post_data["output_folder"]

        for data in self.dataset:
            model = HeatModel(data["init_bems_data"]["floor"], self.simulation_step, data["init_bems_data"], data["control_data"],data["layout_data"])
            self.models_floor_dic[data["init_bems_data"]["floor"]] = model

    def _str_simulation_state(self):
        print("Simulation starts")
        time.sleep(0.1)
        print("Simulation Calculation Steps: {}".format(self.simulation_step))
        time.sleep(0.1)
        print("Simulation Results Folder: {}".format(self.output_folder))

    def output_agent_json(self):
        for result in self.output_data:
            print('{0}/result{1}.json'.format(self.output_folder,result[0]))
            fw = open('{0}/result{1}.json'.format(self.output_folder,result[0]),'w')
            json.dump(result[1],fw,indent=4)

    def run_simulation(self,key,model):
        for i in tqdm(range(self.simulation_step)):
            if model.terminate:
                break
            else:
                model.step()
        result = (key,model.spaces_agents_list)
        return result

    def run_all_simulations(self):
        start = time.time()
        self._str_simulation_state()
        for key,model in self.models_floor_dic.items():
            for i in tqdm(range(self.simulation_step)):
                if model.terminate:
                    break
                else:
                    model.step()
        elapsed_time = time.time() - start
        print("Simulation finished!")
        print("Simulation time:{}".format(int(elapsed_time)) + "[sec]")

    def run_all_simulations_multi_process(self):
        start = time.time()
        self._str_simulation_state()
        with multiprocessing.Pool(processes=6) as pool:
            args = list(zip(self.models_floor_dic.keys(),self.models_floor_dic.values()))
            self.output_data = pool.starmap(self.run_simulation, args)
        
        self.output_agent_json()
        elapsed_time = time.time() - start
        print("Simulation finished!")
        print("Simulation time:{}".format(int(elapsed_time)) + "[sec]")