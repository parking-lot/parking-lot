class ParkingLot:
    def __init__(self,parkingLot):
        self.time = 0
        self.state = parkingLot

    def isEntrance(self,x,y):
        return (self.state[x][y] == "E")

    def getState(self,x,y):
        return self.state[x][y]
