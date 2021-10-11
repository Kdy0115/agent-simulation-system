from controllers.sml.simulation import SimulationControl
from controllers.cvt.conversion import *
from views.dynamic_output import *
import time
#from multiprocessing import Pool,freeze_support, RLock
import multiprocessing as mp
from tqdm import tqdm

dataset = DataSet(config_bems, config_control, config_layout, config_simulation)
dataset.integrate_files()


simulation = SimulationControl(dataset.post_data)
# simulation.run_all_simulations()
result = simulation.run_all_simulations_multi_process()
dataset.output_data(result)
