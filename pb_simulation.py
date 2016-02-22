from pb_grid import *
from pb_preference import *
from pb_car import *
import copy

class Simulation:
    def __init__(self, outputFileName):
        self.time = 0
        self.f = open(outputFileName, 'w')
        self.grid = Grid()
        self.carQueue = []
        self.carList = []
        self.prefList = []

    def closeFile(self):
        self.f.close()

    def loadMapFromFile(self, fileName):
        self.grid.readFromFile(fileName)

    def loadCars(self, fileName):
        # Car(entrance, enteringTime, stayingTime, preference)
        car01 = Car((8,0), 0, 100, 1)
        self.carQueue.append(car01)
        car02 = Car((8,0), 2, 100, 1)
        self.carQueue.append(car02)
        car03 = Car((8,0), 4, 100, 2)
        self.carQueue.append(car03)
        car04 = Car((8,0), 7, 100, 1)
        self.carQueue.append(car04)
        car05 = Car((8,0), 8, 10, 2)
        self.carQueue.append(car05)

    def addPreferences(self):
        pref = Preference_00()
        pref.loadGrid(self.grid)
        pref.createPriorityList()
        self.prefList.append(copy.deepcopy(pref))

        pref2 = Preference_01()
        pref2.loadGrid(self.grid)
        eList = self.grid.entranceList()
        pref2.createPriorityList(eList[0])
        self.prefList.append(copy.deepcopy(pref2))

        pref2 = Preference_02()
        pref2.loadGrid(self.grid)
        eList = self.grid.entranceList()
        pref2.createPriorityList(eList[0])
        self.prefList.append(copy.deepcopy(pref2))


    def advanceTimeStep(self):
        # Update position of the current cars
        for car in self.carList:
            if car.pathList:
                car.pos = car.pathList.pop()

        # Inserting car.
        for car in self.carQueue:
            if car.time_in == self.time:
                print car.pref
                car.parkPos = self.prefList[car.pref].getParkingSpot()
                car.pathList = self.grid.findPathBFS(car.pos, car.parkPos[1])
                self.carList.append(car)

        self.time += 1

    def debugOut(self):
        print "time:"
        print self.time
        cnt = 0
        for car in self.carList:
            print cnt
            print car.pos
            self.output()
            cnt += 1

    def output(self):
        f = self.f

        grid = self.grid
        for x in range(0, grid.width):
            for y in range(0, grid.height):
                cell = grid.grid[(x,y)]
                wstr = cell.cellType[0]

                if cell.cellType == 'EXIT':
                    wstr = 'X'
                for car in self.carList:
                    if car.pos == (x,y):
                        wstr = 'C'
                #if wstr == 'R' or wstr == 'P':
                if cell.up:
                    wstr += 'u'
                if cell.down:
                    wstr += 'd'
                if cell.left:
                    wstr += 'l'
                if cell.right:
                    wstr += 'r'

                cnt = 0
                for car in self.carList:
                    if car.pos == (x,y):
                        wstr += str(cnt)
                    cnt += 1

                if cell.cellType == 'GOAL':
                    wstr = 'G0'

                f.write(wstr + ',')
            f.write('\n')

        f.write('!\n')
        return None

