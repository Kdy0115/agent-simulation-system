from controllers.sml.extension.spaces.space_extension import ContinuousSpace3d
from mesa.time import SimultaneousActivation
from mesa import Agent, Model
from controllers.sml.inc.define import *
import numpy as np
import random
import math
from datetime import datetime, timedelta

class Space(Agent):
    capacity = SPACE_HEAT_CAPACITY
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, pos, temp):
        super().__init__(unique_id, model)
        self.pos = pos
        self.temp = temp
        self.energy = self.temp * self.capacity

    def exchange_heat(self):
        neighbor_spaces = self.model.grid.get_neighbors(self.pos, 1, include_center=False)
        for other in neighbor_spaces:
            if other.__class__.__name__ == "Space":
                sum_heat = abs(self.temp - other.temp) * ALPHA
                if self.temp > other.temp:
                    other.energy += sum_heat
                    other.temp += sum_heat/self.capacity
                    self.energy  -= sum_heat
                    self.temp  -= sum_heat/self.capacity

    def output_space_agent(self):
        agent_data = {
            "id"    : self.unique_id,
            "temp"  : self.temp,
            "x"     : self.pos[0],
            "y"     : self.pos[1],
            "z"     : self.pos[2],
        }
        self.model.per_time_dic["agent_list"].append(agent_data)

    def step(self):
        self.exchange_heat()
        self.output_space_agent()

class HeatSource(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, pos, temp, kind):
        super().__init__(unique_id, model)
        self.pos = pos
        self.temp = temp
        self.kind = kind
        if self.kind == 1:
            self.capacity = WINDOW_HEAT_CAPACITY
        else:
            self.capacity = OTHER_SOURCE_HEAT_CAPACITY
        self.energy = self.temp * self.capacity

    def radiant_heat(self):
        neighbor_spaces = self.model.grid.get_neighbors(
            self.pos,
            1,
            include_center=False)
        for other in neighbor_spaces:
            if other.__class__.__name__ == "Space":
                sum_heat = abs(self.temp - other.temp) * GAMMA
                if self.temp > other.temp:
                    other.energy += sum_heat
                    other.temp += sum_heat/other.capacity
                    self.energy -= sum_heat
                    self.temp  -= sum_heat/self.capacity
                else:
                    self.energy += sum_heat
                    self.temp  += sum_heat/self.capacity
                    other.energy -= sum_heat
                    other.temp -= sum_heat/other.capacity
    def step(self):
        self.radiant_heat()

class HeatCharge(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, pos, ac, angle):
        super().__init__(unique_id, model)
        self.pos = pos
        self.direction = ac.direction
        self.speed = ac.verocity
        self.temp = ac.release_temp
        self.angle = angle
        self.radius = INIT_HEAT_CHARGE_RADIUS
        self.change_rate = RATE_OF_CHANGE
        if ac.mode == 1:
            self.energy = -INIT_AC_ENERGY * ac.release_temp
        else:
            self.energy = INIT_AC_ENERGY * ac.release_temp

    def move(self):
        new_pos = (
            float(self.pos[0]) + self.speed * math.cos(math.radians(self.angle)) * math.cos(math.radians(self.direction)),
            float(self.pos[1]) + self.speed * math.sin(math.radians(self.angle)) * math.cos(math.radians(self.direction)),
            float(self.pos[2]) - self.speed * math.sin(math.radians(self.direction))
        )
        self.speed  *= self.change_rate
        self.radius *= (1 + self.change_rate)
        self.model.grid.move_agent(self,new_pos)
        if self.out_of_spaces() or self.convergence_verocity() or self.convergence_energy():
            self.model.remove_agents_list.append(self)

    def convergence_verocity(self):
        return self.speed <= 0.0001

    def convergence_energy(self):
        return abs(self.energy) < 0.0001
            
    def out_of_spaces(self):
        x,y,z = self.pos
        return (x >= self.model.space_x_max or x <= self.model.space_x_min) or (y >= self.model.space_y_max or y <= self.model.space_y_min) or (z >= self.model.space_z_max or z <= self.model.space_z_min)
                
    def convection_heat(self):
        neighbor_spaces = self.model.grid.get_neighbors(self.pos, int(1 + self.radius), include_center=False)
        for other in neighbor_spaces:
            if self.energy != 0:
                if other.__class__.__name__ == "Space":
                    sum_heat = BETA * abs(self.temp - other.temp) / ((4/3 * math.pi * self.radius**3) * self.model.grid.get_distance(self.pos, other.pos) ** 2)
                    if sum_heat > abs(self.energy):
                        sum_heat = self.energy
                    if self.energy < 0:
                        if self.temp < other.temp:
                            other.energy -= sum_heat
                            other.temp -= sum_heat / SPACE_HEAT_CAPACITY
                            self.energy += sum_heat
                            self.temp  += sum_heat / SPACE_HEAT_CAPACITY
                    else:
                        if self.temp > other.temp:
                            other.energy += sum_heat
                            other.temp   += sum_heat / SPACE_HEAT_CAPACITY
                            self.energy  -= sum_heat
                            self.temp    -= sum_heat / SPACE_HEAT_CAPACITY


    def step(self):
        self.move()
        self.convection_heat()

class AirConditioner(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.direction = WIND_OUTLET_ANGLE
        self.thermo = True
        self.read_control_data()
        self.power = 0

    def read_control_data(self):
        self.set_temp = float(self.model.current_control_data["設定温度0"])
        self.mode     = int(self.model.current_control_data["運転モード0"])
        verocity_label = int(self.model.current_control_data["風速0"])
        if verocity_label == 1:
            verocity = 0.5
        elif verocity_label == 2:
            verocity = 1.0
        elif verocity_label == 3:
            verocity = 1.5
        self.verocity = verocity
        self.release_temp = self.set_temp

    def _switch_thermo(self):
        neighbor_spaces = self.model.grid.get_neighbors(self.pos, 1, include_center=False)
        space_temp_list = []
        for space in neighbor_spaces:
            if space.__class__.__name__ == "Space":
                space_temp_list.append(space.temp)
        observe_temp = sum(space_temp_list)/len(space_temp_list)
        if self.mode == 1:
            if observe_temp - self.set_temp > 0.5:
                self.thermo = False
        elif self.mode == 2:
            if self.set_temp - observe_temp > 0.5:
                self.thermo = False

    def switch_mode(self):
        self._switch_thermo()
        if self.thermo == True:
            self.release_temp = self.set_temp
            self.mode = 3
        else:
            if self.mode == 1:
                self.release_temp = self.set_temp - 10
            elif self.mode == 2:
                self.release_temp = self.set_temp + 20

    def create_heat(self):
        if self.mode != 0:
            for n in range(4):
                heat = HeatCharge(self.model.next_id(), self.model, self.pos, self, 90*n)
                self.model.schedule.add(heat)
                self.model.grid.place_agent(heat, self.pos)
                self.power += INIT_AC_ENERGY * abs(self.release_temp - self.set_temp)

    def step(self):
        if self.model.schedule.steps%60 == 0:
            self.read_control_data()
            #print("設定温度：{0}　運転モード：{1}　風速：{2}　吹き出し温度：{3}".format(self.set_temp,self.mode,self.verocity,self.release_temp))
        self.switch_mode()
        self.create_heat()


class HeatModel(Model):
    """A model with some number of agents.（複数のエージェントを持つHeatModelクラス）

    Args:
        Model (Model): Override from Model class
    """    
    def __init__(self, width, height, depth, floor, simulation_step, control_data):
        """ Model init method.

        Args:
            width (Int): The width of a space
            height (Int): The height of a space
            depth (Int): The depth of a space
            floor (Int): Floor for simulation
            simulation_step (Int): The number of simulation
            control_data (object): Formatted control plan data
        """        
        self.num_agents = width * height * depth
        self.grid = ContinuousSpace3d(width, height, depth, False, -5, -5, -1)
        self.schedule = SimultaneousActivation(self)
        self.floor = floor
        self.simulation_step = simulation_step
        self.control_data = control_data
        self.current_control_data = next(self.control_data)
        self.current_id = 0
        self.space_x_min = 0
        self.space_y_min = 0
        self.space_z_min = 0
        self.space_x_max = width - 5
        self.space_y_max = height - 5
        self.space_z_max = depth - 1
        self.remove_agents_list = []
        self.spaces_agents_list = []
        self.per_time_dic = {}
        self.time = datetime(2020,1,15,15,00,1)

        self.running = True

        for x_i in range(width - 5):
            for y_i in range(height - 5):
                for z_i in range(depth - 1):
                    pos = (x_i, y_i, z_i)
                    if ((z_i == 4) and (x_i == 5 and y_i == 5)) or ((z_i == 4) and (x_i == 10 and y_i == 10)):
                        agent = AirConditioner(self.next_id(),self,pos)
                        self.schedule.add(agent)
                        self.grid.place_agent(agent, pos)
                    if ((z_i == 0 or z_i == depth-2) or (x_i == 0 or x_i == width-6) or (y_i == 0 or y_i == height-6)):
                        agent = HeatSource(self.next_id(),self,pos,30,1)
                    else:
                        agent = Space(self.next_id(),self,pos,random.uniform(18, 20))
                    self.schedule.add(agent)
                    self.grid.place_agent(agent, pos)

    def next_control_data(self):
        self.current_control_data = next(self.control_data)

    def remove_agents(self):
        for agent in self.remove_agents_list:
            self.schedule.remove(agent)
            self.grid.remove_agent(agent)
        self.remove_agents_list = []

    def step(self):
        self.per_time_dic["timestamp"] = self.time.strftime('%Y-%m-%d %H:%M:%S')
        self.per_time_dic["agent_list"] = []
        self.schedule.step()
        if self.schedule.steps%60 == 0:
            self.next_control_data()
            self.spaces_agents_list.append(self.per_time_dic)
        self.remove_agents()
        self.time += timedelta(seconds=1)
        self.per_time_dic = {}
