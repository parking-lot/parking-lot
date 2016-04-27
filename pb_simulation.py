from pb_grid import *
from pb_preference import *
from pb_car import *
import copy
import os

class Simulation:
    # def __init__(self, outputFileName):
    def __init__(self):
        self.time = 0
        self.grid = Grid()
        self.carList = []   # list of all cars (both in and out of the parking lot)
        self.prefs = {} #dictionary of preferences (prefName, preference) key is a str
        self.outputFileName = None
        self.outputFileName_simple = None
        self.latestID = 10000

    def openOutputFile(self):
        self.f = open(self.outputFileName, 'w')
        
    def openOutputFile_simple(self):
        self.f_simple = open(self.outputFileName_simple, 'w')

    def closeOutputFile(self):
        f = self.f
        f.seek(-2,2)
        f.truncate()
        f.write(']}')
        f.close()
        
    def closeOutputFile_simple(self):
        self.f_simple.close()
        
    def setOutputFileName(self, fileName):
        #self.outputFileName = fileName
        self.f = open(fileName, 'w')
        f = self.f
        
        # beginning:
        f.write('{\n')
        
        # map input:
        inputFileName = '\"reallot.map\"'
        f.write('\"map_input\": ')
        f.write(inputFileName)
        f.write(',\n')
        
        # comments:
        comments = '\"comments\"'
        f.write('\"comments\": ')
        f.write(comments)
        f.write(',\n')
        
        # frames open
        f.write('\"frames\": ')
        f.write('[')
        f.write('\n')
        
    def setOutputFileName_simple(self, fileName):
        self.outputFileName_simple = fileName
        self.f_simple = open(fileName, 'w')

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
            self.carList.append(car)
        f.close()

    # returns the id of the car
    def addCars(self, entranceID, goalID, pref):
        car = Car()
        self.latestID += 1
        car.idNum = self.latestID
        car.entranceID = entranceID
        car.goalID = goalID
        car.exitID = entranceID
        car.prefNum = 0
        car.prefName = str(car.prefNum) + str(goalID)
        
        car.time_in = self.time
        car.time_staying = 10000000
        
        self.carList.append(car)
        return car.idNum

    def requestToLeave(self, carID):
        for car in self.carList:
            if car.idNum == carID:
                car.time_staying = self.time - car.time_in
        return 0
    
    def getDirections(self, carID):
        car = None 
        for c in self.carList:
            if c.idNum == carID:
                car = c
                
        if car is None:
            print 'error in getDirections: no car found with ID ' + str(carID)
            return -1
        
        for (x, y) in car.path:
            return -1
            
    def addPreferences(self):
        # 0 : closest to goal
        # 1 : fastest to goal
        # 2 : closest to exit
        # 3 : fastest parking
        
        # adding closest to goal preferences
        for _, goal in self.grid.goals.iteritems():
            # original: pref = Pref_closest_to_goal(self.grid, goal, "closest_to_goal")
            pref = Pref_closest_to_goal(self.grid, goal, "0")
            pref.createPriorityList()
            self.prefs[pref.name] = pref

        # adding temporal closest to goal preferences
        #for _, goal in self.grid.goals.iteritems():
        #    pref = Pref_closest_to_goal_temporal(self.grid, goal, "1", 3.0, 1.0)
        #    pref.createPriorityList()
        #    self.prefs[pref.name] = pref
       
    def advanceTimeStep(self):
        # Update position of the current cars
        print '---- ' + str(self.time) + ' ----'
        
        for car in self.carList:
            # a car entering the parking lot
            if not car.inParkingLot:
                if car.time_in <= self.time and car.status is None:
                    car.pos = self.grid.entrances[car.entranceID].pos
                    pathLength, parkPos = self.prefs[car.prefName].getParkingLengthPos()
                    car.parkPos = parkPos
                    car.pathLength = pathLength
                    car.path = self.grid.findPathBFS(car.pos, parkPos)
                    for (_, pref) in self.prefs.iteritems():
                        pref.removeParkingSpot(car.parkPos)
                    car.status = 'MOVING_TO_PARK_POSITION' 
                    car.inParkingLot = True 
           
            if car.inParkingLot:
                # finished parking
                if ((car.status != "PARKED") and (car.pos == car.parkPos)):
                    car.status = "PARKED"
                    car.time_parked = self.time
                    continue
                
                # find different path if stuck
                if (car.stuck and (car.status != "PARKED") and (car.pos != car.parkPos)):
                    altPath = self.grid.findPathBFS_alternative(car.pos, car.parkPos, car.path[-1])
                    if len(altPath) > 0:
                        car.path = altPath
                   
                # move car to next position
                if car.path:
                    #print car.idNum
                    if len(car.path) == 0:
                        print "path length is 0!!"
                    newPos = car.path[-1]
                    # if the next path is not occupied, move to it position
                    if self.grid.grid[newPos].occupied:
                        car.stuck = True
                    else:
                        self.grid.grid[car.pos].occupied = False
                        car.pos = car.path.pop()
                        self.grid.grid[car.pos].occupied = True
                        car.stuck = False
                    self.grid.grid[car.pos].occupied = True
                
                # Process cars leaving the parking lot
                if car.status == 'PARKED' and (car.getLeaveTime() <= self.time):
                    exit_path = self.grid.findPathBFS_to_exit(car.pos, car.exitID)
                    car.path = exit_path
                    car.status = "LEAVING"
                    self.prefs[car.prefName].readdParkingSpot(car.pos)
                   
                # Car is at exit, remove from parking lot
                if self.grid.isExit(car.pos):
                        #print car.pos
                        self.grid.grid[car.pos].occupied = False
                        car.status = 'LEFT'
                        car.pos = None
                        #print 'car ' + str(car.idNum) + ' left'
                    
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

    def getPrefList(self, prefNum):
        prefList = [[],[],[],[]]
        for car in self.carList:
            prefList[car.prefNum].append(car.idNum)
            
        return str(prefList[prefNum])

    def output(self):
        f = self.f
        
        # frames open
        f.write('{')
        f.write('\n')
        
        # preferences open
        f.write('\"car_prefs": ')
        f.write('[{')
        f.write('\n')
        
        f.write('\"type\": ')
        f.write('0')
        f.write(',\n')
        
        f.write('\"cars\":')
        
        f.write(self.getPrefList(0)) 
        f.write('\n')
        f.write('}')
        
        f.write(', {\n')
        f.write('\"type\": ')
        f.write('1')
        f.write(',\n')
        
        f.write('\"cars\":')
        # TODO placeholder
        f.write('[5,6]')
        f.write('\n')
        f.write('}')
       
        # preferences close
        f.write('],\n')
        
        # car paths open
        f.write('\"car_paths\": ')
        f.write('[')
        f.write('\n')
       
        for car in self.carList:
            f.write('{')
            f.write('\"car\": ')
            f.write(str(car.idNum))
            f.write(',\n')
            f.write('\"path\": ')
            f.write(str(car.path).replace("(", "\"(").replace(")", ")\""))
 
            f.write('},\n')
        
        # car paths close
        f.seek(-2,2)
        f.truncate()
        f.write('],\n')
        
        # map open
        f.write('\"map\": ')
        f.write('\"')
       
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

                if cell.original_direction is not None:
                    wstr += cell.original_direction
                if cell.up and cell.original_direction != 'u':
                    wstr += 'u'
                if cell.down and cell.original_direction !='d':
                    wstr += 'd'
                if cell.left and cell.original_direction != 'l':
                    wstr += 'l'
                if cell.right and cell.original_direction != 'r':
                    wstr += 'r'

                for car in self.carList:
                    if car.pos == (x,y):
                        wstr += str(car.idNum)
                        wstr += 'p'
                        wstr += car.prefName

                f.write(wstr + ',')
            f.write(';')

        # map close
        f.write('\"\n')
        
        # frame close
        f.write('},\n')
        
        #self.closeOutputFile()
        return None
    
    def outputLog(self, logFileName):
        f = open(logFileName, 'w')
        
        # frames open
        f.write('{')
        f.write('\n')
        
        # preferences open
        f.write('\"car_prefs": ')
        f.write('[{')
        f.write('\n')
        
        f.write('\"type\": ')
        f.write('0')
        f.write(',\n')
        
        f.write('\"cars\":')
        
        # TODO placeholder
        f.write(self.getPrefList(0)) 
        f.write('\n')
        f.write('}')
        
        f.write(', {\n')
        f.write('\"type\": ')
        f.write('1')
        f.write(',\n')
        
        f.write('\"cars\":')
        # TODO placeholder
        f.write('[5,6]')
        f.write('\n')
        f.write('}')
       
        # preferences close
        f.write('],\n')
        
        # car paths open
        f.write('\"car_paths\": ')
        f.write('[')
        f.write('\n')
       
        for car in self.carList:
            f.write('{')
            f.write('\"car\": ')
            f.write(str(car.idNum))
            f.write(',\n')
            f.write('\"path\": ')
            f.write(str(car.path))
            f.write('},\n')
        
        # car paths close
        f.seek(-2,2)
        f.truncate()
        f.write('],\n')
        
        # map open
        f.write('\"map\": ')
        f.write('\"')
       
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

                if cell.original_direction is not None:
                    wstr += cell.original_direction
                if cell.up and cell.original_direction != 'u':
                    wstr += 'u'
                if cell.down and cell.original_direction !='d':
                    wstr += 'd'
                if cell.left and cell.original_direction != 'l':
                    wstr += 'l'
                if cell.right and cell.original_direction != 'r':
                    wstr += 'r'

                for car in self.carList:
                    if car.pos == (x,y):
                        wstr += str(car.idNum)
                        wstr += 'p'
                        wstr += car.prefName

                f.write(wstr + ',')
            f.write(';')

        # map close
        f.write('\"\n')
        
        # frame close
        f.write('},\n')
        
        #self.closeOutputFile()
        return None
   
    # returns map data as string
    def getMapStr(self):
        grid = self.grid
        retStr = ''
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

                if cell.original_direction is not None:
                    wstr += cell.original_direction
                if cell.up and cell.original_direction != 'u':
                    wstr += 'u'
                if cell.down and cell.original_direction !='d':
                    wstr += 'd'
                if cell.left and cell.original_direction != 'l':
                    wstr += 'l'
                if cell.right and cell.original_direction != 'r':
                    wstr += 'r'

                for car in self.carList:
                    if car.pos == (x,y):
                        wstr += str(car.idNum)
                        wstr += 'p'
                        wstr += car.prefName

                retStr += wstr + ','
            retStr += wstr + ';\n'
            
        return retStr
    
    def output_simple(self):
        #self.openOutputFile()
        f = self.f_simple
       
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

                if cell.original_direction is not None:
                    wstr += cell.original_direction
                if cell.up and cell.original_direction != 'u':
                    wstr += 'u'
                if cell.down and cell.original_direction !='d':
                    wstr += 'd'
                if cell.left and cell.original_direction != 'l':
                    wstr += 'l'
                if cell.right and cell.original_direction != 'r':
                    wstr += 'r'

                for car in self.carList:
                    if car.pos == (x,y):
                        wstr += str(car.idNum)
                        wstr += 'p'
                        wstr += car.prefName

                f.write(wstr + ',')
            f.write('\n')

        # map close
        f.write('!\n')
        
        return None
 
