from pb_simulation import *

sim = Simulation()
#sim.load_map_from_file('test_map_03.csv')
#sim.load_map_from_file('reallot3.csv')
sim.load_map_from_file('RealMap.map')
#sim.debugOut()
sim.addPreferences()
sim.loadCars('carList_01.csv')
sim.setOutputFileName('output_01.csv')

for i in range(0,10):
    sim.advanceTimeStep()
    #sim.debugOut()
    sim.output()
    print sim.toList()

sim.closeOutputFile()
