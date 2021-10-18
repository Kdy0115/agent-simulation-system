from controllers.sml.simulation import SimulationControl
from controllers.cvt.conversion import *
from views.dynamic_output import *
import time
#from multiprocessing import Pool,freeze_support, RLock
import multiprocessing as mp
from tqdm import tqdm

dataset = DataSet(config_bems, config_control, config_layout, config_simulation, config_mp)
dataset.integrate_files()

simulation = SimulationControl(dataset.post_data)

if dataset.mp_flag:
    if __name__ == '__main__':
        mp.freeze_support()
        result = simulation.run_all_simulations_multi_process()
        dataset.output_data(result)
else:
    result = simulation.run_all_simulations()
    dataset.output_data(result)
