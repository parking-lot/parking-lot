import copy

class Car:
    def __init__(self):
        self.idNum = 0
        self.entranceID = 0
        self.goalID = 0
        self.exitID = 0
        self.time_in = 0
        self.time_in_real = -1
        self.time_parked = 1000000
        self.time_staying = 0
        self.prefName = None
        self.prefNum = 0
        self.pos = None
        self.parkPos = None
        #self.pathList = []
        self.path = []
        self.pathLength = -1
        self.status = None
        self.inParkingLot = False
        self.stuck = False
        self.initialdirection = None
        self.currentdirection = None

    def setGoal(self, parkPos):
        self.parkPos = parkPos

    # If leave time is positive, the probability increases as well.
    def getLeaveTime(self):
        return self.time_parked + self.time_staying
    
    def initialize_from_string(self, line):
        infoList = [carStr.strip() for carStr in line.split(',')]
        self.idNum = int(infoList[0])
        self.entranceID = int(infoList[1])
        self.goalID = int(infoList[2])
        self.exitID = int(infoList[3])
        self.time_in = int(infoList[4])
        self.time_staying = int(infoList[5])
        #self.prefNum = int(infoList[6])
        self.prefNum = 0
        self.prefName = str(self.prefNum) + str(self.goalID)
        
