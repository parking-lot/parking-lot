from pb_grid import *
from pb_preference import *
from pb_car import *
import copy

class Simulation:
    #def __init__(self, outputFileName):
    def __init__(self):
        self.time = 0
        #self.f = open(outputFileName, 'w')
        self.grid = Grid()
        self.carQueue = []  #queue of cars to enter the parking lot
        self.carList = []   #cars current in the parking lot
        self.prefs = {} #dictionary of preferences (prefName, preference) key is a str

    def closeOutputFile(self):
        self.f.close()
        
    def setOutputFileName(self, fileName):
        self.f = open(fileName, 'w')

    def load_map_from_file(self, fileName):
        self.grid.read_from_file(fileName)
        
    # load cars from file
    def loadCars(self, fileName):
        print "loading cars"
        f = open(fileName, 'r')
        next(f)
        for line in f:
            car = Car()
            car.initialize_from_string(line)
            car.pos = self.grid.entrances[car.entranceID].pos
            self.carQueue.append(car)
        f.close()

    def addPreferences(self):
        # adding closest to goal preferences
        for _, goal in self.grid.goals.iteritems():
            pref = Pref_closest_to_goal(self.grid, goal, "closest_to_goal")
            pref.createPriorityList()
            self.prefs[pref.name] = pref

        #pref = Preference_01()
        #pref.loadGrid(self.grid)
        #eList = self.grid.entranceList()
        #pref.createPriorityList(eList[0])
        #self.prefList.append(copy.deepcopy(pref))
        #
        #pref = Preference_02()
        #pref.loadGrid(self.grid)
        #eList = self.grid.entranceList()
        #pref.createPriorityList(eList[0])
        #self.prefList.append(copy.deepcopy(pref))

    def advanceTimeStep(self):
        # Update position of the current cars
        for car in self.carList:
            # finished parking
            if ((car.status != "PARKED") and (car.pos == car.parkPos)):
                car.status = "PARKED"
                car.time_parked = self.time
                continue
          
            # find path every time
            if (car.stuck and (car.status != "PARKED") and (car.pos != car.parkPos)):
                altPath = self.grid.findPathBFS_alternative(car.pos, car.parkPos, car.path[-1])
                if len(altPath) > 0:
                    car.path = altPath
                #car.path = self.grid.findPathBFS_alternative(car.pos, car.parkPos, car.path[-1])
                
            if (car.status == "LEAVING"):
                car.path = self.grid.findPathBFS_to_exit(car.pos, car.exitID)
                
            # move car to next position
            if car.path:
                newPos = car.path[-1]
                # if the next path is not occupied, move to it position
                if self.grid.grid[newPos].occupied:
                    car.stuck = True
                else:
                    self.grid.grid[car.pos].occupied = False
                    car.pos = car.path.pop()
                    self.grid.grid[car.pos].occupied = True
                    car.stuck = False

            # Process cars leaving the parking lot
            if (car.getLeaveTime() <= self.time):
                exit_path = self.grid.findPathBFS_to_exit(car.pos, car.exitID)
                car.path = exit_path
                car.status = "LEAVING"
            
            self.grid.grid[car.pos].occupied = True
            
            # Car left through the exit
            if (car.status == "LEAVING" and len(car.path) == 0):
                self.carList.remove(car)
                self.grid.grid[car.pos].occupied = False
                
        for _, cell in self.grid.grid.iteritems():
            cell.occupied = False
            for car in self.carList:
                if cell.pos == car.pos:
                    cell.occupied = True
                    break
            
        # Inserting car from queue.
        for car in self.carQueue:
            if car.time_in == self.time:
                pathLength, parkPos = self.prefs[car.prefName].getParkingLengthPos()
                car.parkPos = parkPos
                car.pathLength = pathLength
                car.pathLength = pathLength
                car.path = self.grid.findPathBFS(car.pos, parkPos)
                for (_, pref) in self.prefs.iteritems():
                    pref.removeParkingSpot(car.parkPos)
                self.carList.append(car)

        self.time += 1

    def debugOut(self):
        print "time:" + str(self.time)
        cnt = 0
        for car in self.carList:
            if car.pos == car.parkPos[1]:
                print 'car'  + str(cnt) + ' parked:' + str(car.pos)
            else :
                print 'car'  + str(cnt) + ' pos:' + str(car.pos)
            cnt += 1

    def output(self):
        f = self.f

        grid = self.grid
        for x in range(0, grid.height):
            for y in range(0, grid.width):
                cell = grid.grid[(x,y)]
                wstr = cell.cellType[0]

                if cell.cellType == 'PARK':
                    wstr = 'p'

                if cell.cellType == 'WALL':
                    wstr = 'w'

                if cell.cellType == 'ROAD':
                    wstr = 'r'

                if cell.cellType == 'ENTR':
                    wstr = 'e' + str(cell.idNum)

                if cell.cellType == 'EXIT':
                    wstr = 'x' + str(cell.idNum)
                    
                if cell.cellType == 'GOAL':
                    wstr = 'g' + str(cell.idNum)

                for car in self.carList:
                    if car.pos == (x,y):
                        wstr = 'c'
                        if car.pos == car.parkPos:
                            wstr = 'f'

                if cell.up:
                    wstr += 'u'
                if cell.down:
                    wstr += 'd'
                if cell.left:
                    wstr += 'l'
                if cell.right:
                    wstr += 'r'

                for car in self.carList:
                    if car.pos == (x,y):
                        wstr += str(car.idNum)
                        wstr += 'p'
                        wstr += car.prefName

                f.write(wstr + ',')
            f.write('\n')

        f.write('!\n')
        return None

