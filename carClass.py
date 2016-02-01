import MapObject
    
class Car:
    carCount = 0

    def __init__(self,parkingLot):
        width = len(parkingLot.state[0])
        i = 0
        j = 0
        while (not(parkingLot.isEntrance(i,j))):
            if (i < width): i+=1
            else:
                i = 0
                j+=1
                
        self.location = parkingLot.getState(i,j)
        self.entryTime = parkingLot.time
        self.currentInstruction = self.location
        
        
        Car.carCount += 1
    
    def moveCar(self, newLoc):
        self.location = newLoc

PL = MapObject.ParkingLot([["R","R","R"],["E","R","R"],["X","R","R"]])
C1 = Car(PL)
        
    
