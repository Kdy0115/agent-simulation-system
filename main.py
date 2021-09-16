from controllers.sml.simulation import SimulationControl
from controllers.cvt.conversion import dataset

simulation = SimulationControl(dataset.post_data)
# simulation.run_all_simulations()
simulation.run_all_simulations_multi_process()

