from controllers.sml.simulation import SimulationControl
from controllers.cvt.conversion import dataset

simulation = SimulationControl(10,dataset)
simulation.run_all_simulations()