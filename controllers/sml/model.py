from controllers.sml.extension.spaces.space_extension import ContinuousSpace3d
from mesa.time import SimultaneousActivation
from mesa import Agent, Model
from controllers.sml.inc.define import *
import numpy as np
import random
import math
import copy
from datetime import datetime, timedelta

class Space(Agent):
    capacity = SPACE_HEAT_CAPACITY
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, pos, temp):
        super().__init__(unique_id, model)
        self.pos = pos
        self.temp = temp
        self.energy = self.temp * self.capacity
        self.neighbors_list = []

    def exchange_heat(self):
        # neighbor_spaces = self.model.grid.get_neighbors(self.pos, 1, include_center=False)
        if len(self.neighbors_list) < 1:
            self.neighbors_list = self.model.grid.get_neighbors(self.pos, 1, include_center=False)
        for other in self.neighbors_list:
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
            "class" : "space"
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
        elif self.kind == 5:
            self.capacity = 1
        else:
            self.capacity = OTHER_SOURCE_HEAT_CAPACITY
        self.energy = self.temp * self.capacity
        self.neighbors_list = []

    def radiant_heat(self):
        if len(self.neighbors_list) < 1:
            self.neighbors_list = self.model.grid.get_neighbors(self.pos, 1, include_center=False)
        for other in self.neighbors_list:
            if other.__class__.__name__ == "Space":
                if self.kind == 5:
                    sum_heat = abs(self.temp - other.temp) * HUMAN_HEAT_RATIO
                    if self.temp > other.temp:
                        other.energy += sum_heat
                        other.temp += sum_heat / other.capacity
                else:
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
        # y-z平面の向き
        self.direction = ac.direction
        self.speed = ac.verocity
        self.temp = ac.release_temp
        # x-y座標の向き
        self.angle = angle
        self.radius = INIT_HEAT_CHARGE_RADIUS
        self.change_rate = RATE_OF_CHANGE
        self.ac = ac
        if ac.mode == 1:
            self.energy = -INIT_AC_ENERGY * ac.release_temp
        else:
            self.energy = INIT_AC_ENERGY * ac.release_temp
        self.pre_energy = self.energy

    def move(self):
        new_pos = (
            float(self.pos[0]) + self.speed * math.cos(math.radians(self.angle)) * math.cos(math.radians(self.direction)),
            float(self.pos[1]) + self.speed * math.sin(math.radians(self.angle)) * math.cos(math.radians(self.direction)),
            float(self.pos[2]) - self.speed * math.sin(math.radians(self.direction))
        )
        self.speed  *= self.change_rate
        if self.radius >= 5:
            self.radius = 5
        else:
            self.radius *= (1 + self.change_rate)
        
        if not self.out_of_spaces(new_pos):
            self.model.grid.move_agent(self,new_pos)
        # if self.out_of_spaces() or self.convergence_verocity() or self.convergence_energy():
        #     self.model.remove_agents_list.append(self)

    def add_remove_agents(self):
        if self.out_of_spaces(self.pos) or self.convergence_verocity() or self.convergence_energy() or self.check_change_energy():
            # self.model.remove_agents_list.append(self)
            self.model.remove_agents_set.add(self.unique_id)

    def check_change_energy(self):
        check = self.energy*self.pre_energy <= 0
        self.pre_energy = self.energy
        return check

    def convergence_verocity(self):
        return self.speed <= 0.01

    def convergence_energy(self):
        return abs(self.energy) < 0.0001
            
    def out_of_spaces(self,pos):
        x,y,z = pos
        return (x >= self.model.space_x_max or x <= self.model.space_x_min) or (y >= self.model.space_y_max or y <= self.model.space_y_min) or (z >= self.model.space_z_max or z <= self.model.space_z_min)
                
    def convection_heat(self):
        neighbor_spaces = self.model.grid.get_neighbors(self.pos, int(1 + self.radius), include_center=False)
        for other in neighbor_spaces:
            if self.energy != 0:
                if other.__class__.__name__ == "Space":
                    sum_heat = BETA * abs(self.temp - other.temp) / ((4/3 * math.pi * self.radius**3) * self.model.grid.get_distance(self.pos, other.pos) ** 2)
                    # print("渡すエネルギー：{}".format(sum_heat))
                    # print("熱荷温度：{}".format(self.temp))
                    # print("空間温度：{}".format(other.temp))
                    if sum_heat > abs(self.energy):
                        sum_heat = abs(self.energy)
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

    def collision_barrier(self):
        neighbor_barriers = self.model.grid.get_neighbors(self.pos, int(self.radius - 1), include_center=False)
        for barrier in neighbor_barriers:
            if barrier.__class__.__name__ == "HeatSource":
                if (self.energy < 0 and self.temp < barrier.temp) or (self.energy > 0 and self.temp > barrier.temp):
                    energy = self.energy * GAMMA
                    barrier.energy += energy
                    barrier.temp += energy / barrier.capacity
                    # self.model.remove_agents_list.append(self)
                    self.model.remove_agents_set.add(self.unique_id)
                    break

    def heat_collision(self):
        def _decision_angle(agt1,agt2):
            if agt1.speed > agt2.speed:
                angle = agt1.angle
                speed = agt1.speed
            else:
                angle = agt2.angle
                speed = agt2.speed
            if agt1.angle != agt2.angle:
                speed = abs(agt1.speed - agt2.speed)
            
            return angle,speed
            

        neighbor_spaces = self.model.grid.get_neighbors(self.pos, int(self.speed + self.radius), include_center=False)
        for other in neighbor_spaces:
            if other.__class__.__name__ == "HeatCharge":
                d = self.model.grid.get_distance(other.pos, self.pos)
                # 衝突条件を満たすとき
                if d < (other.radius + self.radius):
                    # print(self.temp,other.temp)
                    angle,speed = _decision_angle(self,other)
                    if self.radius > other.radius:
                        self.angle = angle
                        self.speed = speed
                        self.energy = (other.energy + self.energy) / 2
                        # self.temp += other.energy / SPACE_HEAT_CAPACITY
                        self.temp = (self.temp + other.temp) / 2
                        # self.model.remove_agents_list.append(other)
                        self.model.remove_agents_set.add(other.unique_id)
                        # print(self.temp)
                    else:
                        other.angle = angle
                        other.speed = speed
                        other.energy = (self.energy + other.energy) / 2
                        # other.temp += self.energy / SPACE_HEAT_CAPACITY
                        other.temp = (self.temp + other.temp) / 2
                        # self.model.remove_agents_list.append(self)
                        self.model.remove_agents_set.add(self.unique_id)
                    break


    def output_space_agent(self):
        agent_data = {
            "id"    : self.unique_id,
            "temp"  : self.temp,
            "x"     : self.pos[0],
            "y"     : self.pos[1],
            "z"     : self.pos[2],
            "class" : "heat_charge"
        }
        self.model.per_time_dic["agent_list"].append(agent_data)

    def step(self):
        self.move()
        self.heat_collision()
        self.collision_barrier()
        self.convection_heat()
        self.add_remove_agents()
        self.output_space_agent()

class AirConditioner(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, pos, ac_id, observe_temp):
        super().__init__(unique_id, model)
        self.pos = pos
        self.direction = WIND_OUTLET_ANGLE
        self.thermo = True
        self.ac_id = ac_id
        self.read_control_data()
        self.power = 0
        self.observe_temp = observe_temp
        self.model = model
        model.ac_agents_list.append(self)

    def output_ac_data(self):
        agent_data = {
            "id"            : self.unique_id,
            "ac_id"         :self.ac_id,
            "observe_temp"  : self.observe_temp,
            "x"             : self.pos[0],
            "y"             : self.pos[1],
            "z"             : self.pos[2],
            "release_temp"  : self.release_temp,
            "mode"          : self.mode,
            "setting_temp"  : self.set_temp,
        }
        self.model.per_time_dic["agent_list"].append(agent_data)

    def read_control_data(self):
        self.set_temp = float(self.model.current_control_data["{}設定温度".format(self.ac_id)])
        self.mode     = int(self.model.current_control_data["{}運転モード".format(self.ac_id)])
        verocity_label = int(self.model.current_control_data["{}風速".format(self.ac_id)])
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
            else:
                self.thermo = True
        elif self.mode == 2:
            if self.set_temp - observe_temp > 0.5:
                self.thermo = False
            else:
                self.thermo = True
        self.observe_temp = observe_temp

    def switch_mode(self):
        self._switch_thermo()
        if self.thermo == True and self.mode != 0:
            self.release_temp = self.observe_temp
            self.mode = 3
        else:
            if self.mode == 1:
                self.release_temp = self.set_temp - 10
            elif self.mode == 2:
                self.release_temp = self.set_temp + 20
            elif self.mode == 3:
                self.release_temp = self.observe_temp

    def create_heat(self):
        if self.mode != 0:
            for n in range(4):
                heat = HeatCharge(self.model.next_id(), self.model, self.pos, self, 90*n)
                self.model.schedule.add(heat)
                self.model.grid.place_agent(heat, self.pos)
                self.power += INIT_AC_ENERGY * abs(self.release_temp - self.set_temp)
                # print("熱荷温度：{0}熱荷エネルギー{1}".format(heat.temp,heat.energy))


    def see_class(self):
        print("時間：{}".format(self.model.time))
        print("-----------------------------------------------")
        print("空調{}".format(self.ac_id))
        print("-----------------------------------------------")
        print("観測温度：{}".format(self.observe_temp))
        print("サーモ：{}".format(self.thermo))
        print("運転モード：{}".format(self.mode))
        print("吹き出し温度：{}".format(self.release_temp))
        print("設定温度：{}".format(self.set_temp))
        print("風速：{}".format(self.verocity))

    def step(self):
        if self.model.schedule.steps%60 == 0:
            self.read_control_data()
            self.switch_mode()
        # self.see_class()
        self.create_heat()
        self.output_ac_data()


class HeatModel(Model):
    """A model with some number of agents.（複数のエージェントを持つHeatModelクラス）

    Args:
        Model (Model): Override from Model class
    """    
    def __init__(self,floor, simulation_step, init_bems_data, control_data, layout_data, source_data):
        """ Model init method.

        Args:
            width (Int): The width of a space
            height (Int): The height of a space
            depth (Int): The depth of a space
            floor (Int): Floor for simulation
            simulation_step (Int): The number of simulation
            init_ebms_data(object): Formatted init simulation data
            control_data (object): Formatted control plan data
            layout_data (object): Formatted layout data
        """        
        self.current_id =  0
        self.running = True
        self.terminate = False

        self.layout_data = layout_data["layout"]
        self.source_data = source_data["data"]
        
        self.ac_position = layout_data["ac"]

        self.bems_data_num = 0
        self.all_bems_data = init_bems_data["bems_data"]
        self.init_bems_data = self.all_bems_data[self.bems_data_num]
        self.bems_data_num += 1

        self.floor = floor
        self.simulation_step = simulation_step

        self.control_data = control_data
        self.current_control_data = next(self.control_data)


        # self.remove_agents_list = []
        self.remove_agents_set = set()
        self.spaces_agents_list = []
        self.heat_charge_agents_list = []
        self.ac_agents_list = []
        self.per_time_dic = {}

        self.time = datetime.strptime(self.init_bems_data["時間"].replace("/","-"), '%Y-%m-%d %H:%M:%S')

        self.source_data_info = -1

        self._set_space_param()

    def _set_ac_agent(self):
        for one in self.ac_position:
            pos = (float(one["x"]),float(one["y"]),float(one["z"]))
            agent = AirConditioner(self.next_id(),self,pos,one["id"],self.init_bems_data["{}吸込温度".format(one["id"])])
            self.schedule.add(agent)
            self.grid.place_agent(agent, pos)

    def _general_set_agent_roop(self,pos,x_i,y_i,z_i,base_temp):
        if (z_i == self.space_z_min) or (z_i == self.space_z_max) or (x_i == self.space_x_min) or (x_i == self.space_x_max) or (y_i == self.space_y_min) or (y_i == self.space_y_max):
            agent = HeatSource(self.next_id(),self,pos,base_temp,1)
        else:
            agent = Space(self.next_id(),self,pos,base_temp)
        self.schedule.add(agent)
        self.grid.place_agent(agent, pos)

    def _init_agents_position(self):
        base_point = [value for value in self.layout_data if (value["x"] != self.space_x_min-2) and (value["y"] != self.space_y_min-2) and (value["x"] != self.space_x_max-4) and (value["y"] != self.space_y_max-4)][0]
        if len(base_point) == 0:
            x_condition = ""
            y_condition = ""
        else:
            for value in self.layout_data:
                if value["x"] == base_point["x"]:
                    if value["y"] <= base_point["y"]:
                        y_condition = "small"
                    else:
                        y_condition = "big"
                if value["y"] == base_point["y"]:
                    if value["x"] <= base_point["x"]:
                        x_condition = "big"
                    else:
                        x_condition = "small"
            base_point["x"] += 3
            base_point["y"] += 3

        for x_i in range(self.space_x_min,self.space_x_max + 1):
            for y_i in range(self.space_y_min,self.space_y_max + 1):
                for z_i in range(self.space_z_min,self.space_z_max + 1):
                    pos = (x_i,y_i,z_i)
                    pos_format = (float(x_i),float(y_i),float(z_i))
                    distance_arr = []
                    for i in self.ac_agents_list:
                        distance_arr.append(self.grid.get_distance(i.pos,pos_format))
                    base_temp = self.ac_agents_list[distance_arr.index(min(distance_arr))].observe_temp
                    source_temp = -1
                    for i in range(len(self.source_data)):
                        if (self.source_data[i]["x"] + self.space_x_min == x_i) and (self.source_data[i]["y"] + self.space_y_min == y_i) and (self.source_data[i]["z"] == z_i):
                            source_temp = self.source_data[i]["temp"]
                    if x_condition == "big" and y_condition == "big":
                        if source_temp > 0:
                            agent = HeatSource(self.next_id(), self, pos, source_temp, 5)
                            self.schedule.add(agent)
                            self.grid.place_agent(agent, pos)                            
                        elif (x_i > base_point["x"] and y_i > base_point["y"]):
                            if (x_i == base_point["x"] + 1) or (y_i == base_point["y"] + 1):
                                if  z_i > 0 and z_i < 4:
                                    agent = HeatSource(self.next_id(),self,pos,base_temp,1)
                                    self.schedule.add(agent)
                                    self.grid.place_agent(agent, pos)
                        else:
                            self._general_set_agent_roop(pos,x_i,y_i,z_i,base_temp)
                    elif x_condition == "big" and y_condition == "small":
                        if source_temp > 0:         
                            agent = HeatSource(self.next_id(), self, pos, source_temp, 5)
                            self.schedule.add(agent)
                            self.grid.place_agent(agent, pos)                                        
                        elif (x_i > base_point["x"] and y_i < base_point["y"]):
                            if (x_i == base_point["x"] + 1) or (y_i == base_point["y"] - 1):
                                if  z_i > 0 and z_i < 4:
                                    agent = HeatSource(self.next_id(),self,pos,base_temp,1)
                                    self.schedule.add(agent)
                                    self.grid.place_agent(agent, pos)
                        else:
                            self._general_set_agent_roop(pos,x_i,y_i,z_i,base_temp)
                    elif x_condition == "small" and y_condition == "big":
                        if source_temp > 0:
                            agent = HeatSource(self.next_id(), self, pos, source_temp, 5)
                            self.schedule.add(agent)
                            self.grid.place_agent(agent, pos)                                         
                        elif (x_i < base_point["x"] and y_i > base_point["y"]):
                            if (x_i == base_point["x"] - 1) or (y_i == base_point["y"] + 1):
                                if  z_i > 0 and z_i < 4:
                                    agent = HeatSource(self.next_id(),self,pos,base_temp,1)
                                    self.schedule.add(agent)
                                    self.grid.place_agent(agent, pos)
                        else:
                            self._general_set_agent_roop(pos,x_i,y_i,z_i,base_temp)
                    elif x_condition == "small" and y_condition == "small":
                        if source_temp > 0:          
                            agent = HeatSource(self.next_id(), self, pos, source_temp, 5)
                            self.schedule.add(agent)
                            self.grid.place_agent(agent, pos)                                         
                        elif (x_i < base_point["x"] and y_i < base_point["y"]):
                            if (x_i == base_point["x"] - 1) or (y_i == base_point["y"] - 1):
                                if  z_i > 0 and z_i < 4:
                                    agent = HeatSource(self.next_id(),self,pos,base_temp,1)
                                    self.schedule.add(agent)
                                    self.grid.place_agent(agent, pos)
                        else:
                            self._general_set_agent_roop(pos,x_i,y_i,z_i,base_temp)
                    else:
                        if source_temp > 0:
                            agent = HeatSource(self.next_id(), self, pos, source_temp, 5)
                            self.schedule.add(agent)
                            self.grid.place_agent(agent, pos)                                
                        else:                          
                            self._general_set_agent_roop(pos,x_i,y_i,z_i,base_temp)

    def _set_space_param(self):
        grid_points = self.layout_data
        x_arr = []
        y_arr = []
        for value in grid_points:
            x_arr.append(value["x"])
            y_arr.append(value["y"])
        min_x,max_x = min(x_arr),max(x_arr)
        min_y,max_y = min(y_arr),max(y_arr)
        min_z,max_z = 0,4

        self.grid = ContinuousSpace3d(max_x + 6, max_y + 6, max_z, False, min_x, min_y, min_z)
        self.space_x_min = min_x + 2
        self.space_y_min = min_y + 2
        self.space_z_min = min_z
        self.space_x_max = max_x + 4
        self.space_y_max = max_y + 4
        self.space_z_max = max_z
        self.width = self.space_x_max - self.space_x_min
        self.height = self.space_y_max - self.space_y_min
        self.depth = self.space_z_max - self.space_z_min

        self.schedule = SimultaneousActivation(self)

        self._set_ac_agent()
        self._init_agents_position()

    def next_control_data(self):
        try:
            self.current_control_data = next(self.control_data)
        except StopIteration:
            self.terminate = True

    def _reset_heat_source_temp(self):
        for agent in self.grid._index_to_agent.values():
            if agent.__class__.__name__ =="HeatSource":
                x_i,y_i,z_i = agent.pos
                pos_format = (float(x_i),float(y_i),float(z_i))
                distance_arr = []
                for i in self.ac_agents_list:
                    distance_arr.append(self.grid.get_distance(i.pos,pos_format))
                base_id = self.ac_agents_list[distance_arr.index(min(distance_arr))].ac_id
                agent.temp = self.init_bems_data["{}吸込温度".format(base_id)]

    def check_next_bems_data(self):
        if len(self.all_bems_data) > self.bems_data_num:
            cmp_time = datetime.strptime(self.all_bems_data[self.bems_data_num]["時間"].replace("/","-"), '%Y-%m-%d %H:%M:%S')
            if self.time == cmp_time:
                self.init_bems_data = self.all_bems_data[self.bems_data_num]
                self._reset_heat_source_temp()
                self.bems_data_num += 1

    def remove_agents(self):
        remove_list = []
        for one in self.grid._index_to_agent.values():
            if one.unique_id in list(self.remove_agents_set):
                remove_list.append(one)

        for agent in remove_list:
            self.schedule.remove(agent)
            self.grid.remove_agent(agent)

        self.remove_agents_set = set()

    def print_state(self):
        print("時間：{}".format(self.time))

    def step(self):
        if not self.terminate:
            self.check_next_bems_data()
            self.per_time_dic["timestamp"] = self.time.strftime('%Y-%m-%d %H:%M:%S')
            # self.per_time_dic["timestamp"] = self.time
            self.per_time_dic["agent_list"] = []
            self.schedule.step()
            if self.time.second == 0:
                self.next_control_data()
                self.spaces_agents_list.append(self.per_time_dic)
                # self.print_state()
            # print(self.schedule.get_agent_count())
            self.remove_agents()
            self.time += timedelta(seconds=1)
            self.per_time_dic = {}
