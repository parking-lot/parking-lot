from pb_simulation import *

sim = Simulation()
sim.load_map_from_file('RealMap.map')
sim.addPreferences()
sim.loadCars('carList_tiny.csv')
sim.setOutputFileName('output_01.csv')
#sim.setOutputFileName_simple('output_01.csv')

extraCarID = -1
for i in range(0,50):
    if i == 10:
        extraCarID = sim.addCars(0,0,0)
        print 'a new car added with ID ' + str(extraCarID)
       
    if i == 20:
        sim.requestToLeave(extraCarID)
        print 'the new car with ID ' + str(extraCarID) + ' is leaving the parking lot'
        
    sim.advanceTimeStep()
    
    #sim.getTime()
    sim.output()
    #sim.output_simple()
    #print sim.getPath(0)
    #sim.output()
    #print sim.toList()
    #print sim.getMapStr()

sim.closeOutputFile()
#sim.closeOutputFile_simple()
