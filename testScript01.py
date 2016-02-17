from pb_simulation import *

sim = Simulation()
sim.loadMapFromFile('test_map_01.txt')
sim.addPreference_1()
sim.loadCars('temp')

for i in range(0,30):
    sim.advanceTimeStep()
    sim.debugOut()
