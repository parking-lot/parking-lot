from pb_simulation import *

sim = Simulation()
sim.load_map_from_file('RealMap.map')
sim.addPreferences()
sim.loadCars('carList_small.csv')
sim.setOutputFileName('output_01.csv')
#sim.setOutputFileName_simple('output_01.csv')

for i in range(0,1):
    if i == 10:
        sim.addCars(0,0,0)
        
    sim.advanceTimeStep()
    
    #sim.addcar()
    #sim.requestToLeave(id, exitNum)
    #sim.getTime()
    sim.output()
    #sim.output_simple()
    #print sim.getPath(0)
    #sim.debugOut()
    #sim.output()
    #print sim.toList()
    #print sim.getMapStr()

sim.closeOutputFile()
#sim.closeOutputFile_simple()
