from pb_simulation import *

sim = Simulation()
#sim.load_map_from_file('test_map_03.csv')
sim.load_map_from_file('reallot3.csv')
#sim.debugOut()
sim.addPreferences()
sim.loadCars('carList_01.csv')
sim.setOutputFileName('output_01.csv')

sim.grid.findPathBFS((16,8),(11,19))

for i in range(0,200):
    sim.advanceTimeStep()
    #sim.debugOut()
    sim.output()

sim.closeOutputFile()
