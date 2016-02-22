from pb_simulation import *

sim = Simulation('test_out02.txt')
sim.loadMapFromFile('test_map_02.txt')
sim.addPreferences()
sim.loadCars('temp')

for i in range(0,40):
    sim.advanceTimeStep()
    sim.debugOut()
#sim.output('temp')

sim.closeFile()
