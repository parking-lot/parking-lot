from pb_simulation import *

sim = Simulation('morewood_out03.txt')
sim.loadMapFromFile('../maps/morewood.map')
#sim.debugOut()
sim.addPreferences()
sim.loadCars('temp')

for i in range(0,40):
    sim.advanceTimeStep()
    sim.debugOut()

sim.closeFile()
