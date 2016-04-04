from pb_simulation import *

sim = Simulation('test_out03.txt')
sim.loadMapFromFile('test_map_03.txt')
sim.debugOut()
sim.addPreferences()
sim.loadCars('carList_01.csv')


for i in range(0,80):
    sim.advanceTimeStep()
    sim.debugOut()

sim.closeFile()
