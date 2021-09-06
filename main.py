from controllers.sml.simulation import SimulationControl
from controllers.cvt.conversion import dataset

simulation = SimulationControl(120,dataset)
simulation.run_all_simulations()