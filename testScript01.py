from pb_simulation import *

sim = Simulation('test_out03.txt')
sim.loadMapFromFile('test_map_03.txt')
sim.debugOut()
sim.addPreferences()
sim.loadCars('temp')

for i in range(0,40):
    sim.advanceTimeStep()
    sim.debugOut()

sim.closeFile()
