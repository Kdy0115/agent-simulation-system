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

class Simulation(Process):

    def __init__(self, num, model, output_folder, floor):
        """ コンストラクタ

        Args:
            num ([type]): [description]
            model ([type]): [description]
            output_folder ([type]): [description]
            floor ([type]): [description]
        """        
        super().__init__()
        self.__num = num
        self.__model = model
        self.__output_folder = output_folder
        self.__floor = floor

    def output_agent_json(self):
        fw = open('{0}/result{1}.json'.format(self.__output_folder,self.__floor),'w')
        json.dump(self.__model.spaces_agents_list,fw,indent=4)

    def run_simulation(self, num: int, model):
        for i in tqdm(range(num)):
            model.step()
        return model

    def run(self):
        self.run_simulation(self.__num, self.__model)
        self.output_agent_json()


class SimulationControl():

    def __init__(self,dataset):
        #self.floors = [4,5]
        self.simulation_step = dataset.simulation_step
        self.models_floor_dic = {}
        self.dataset = dataset.simulation_data
        self.output_folder = self.dataset.output_folder

        for data in self.dataset:
            condition = {
                "x":{
                    "relation":">=",
                    "value"   :18
                },
                "y":{
                    "relation": ">",
                    "value"   : 4,
                },
            }
            model = HeatModel(25, 25, 6, data["init_bems"]["floor"], self.simulation_step, self.dataset.control_data,condition)
            self.models_floor_dic["{}F".format(floor)] = model

    def _str_simulation_state(self):
        print("Simulation starts")
        time.sleep(0.1)
        print("Simulation Floors: {}.".format(self.floors))
        time.sleep(0.1)
        print("Simulation Calculation Steps: {}".format(self.simulation_step))
        time.sleep(0.1)
        print("Simulation Results Folder: {}".format(self.output_folder))

    def run_all_simulations(self):
        start = time.time()
        processes = []
        self._str_simulation_state()
        for key,model in self.models_floor_dic.items():
            # print("Simulation number {} is running.".format(cnt))
            process = Simulation(self.simulation_step, model, self.output_folder, key)
            process.start()
            processes.append(process)
            # for i in tqdm(range(self.simulation_step)):
            #     model.step()
        # print(processes[0].model)
        # exit()
        cnt = 1
        print()
        for p in processes:
            p.join()
            # self.output_agent_json(key,p.__model)
        elapsed_time = time.time() - start
        print("Simulation finished!")
        print("Simulation time:{}".format(int(elapsed_time)) + "[sec]")