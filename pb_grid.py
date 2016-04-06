import copy
import Queue

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

class Cell:
    def __init__(self, (x, y), cellType):
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.cellType = None
        self.neighbors = [] # stores the POSITION (x,y), NOT the cells.
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        
        self.newUp = False      # These new directions are used only to create the grid.
        self.newDown = False
        self.newLeft = False
        self.newRight = False
        
        self.occupied = False
        #self.goalName = None
        self.idNum = 0;

    def __str__(self):
        if self.cellType == "WALL":
            prt = "WALL"
            return prt
        if self.cellType == "ROAD":
            prt = "ROAD"
            if self.up:
                prt += " UP"
            if self.down:
                prt += " DOWN"
            if self.left:
                prt += " LEFT"
            if self.right:
                prt += " RIGHT"
            return prt + self.neighbors.__str__()
        if self.cellType == "PARK":
            prt = "PARK"
            if self.occupied:
                prt += " FULL"
            else:
                prt += " EMPTY"
            return prt
        if self.cellType == "GOAL":
            prt = "GOAL "
            return prt + self.goalName
        if self.cellType == "EXIT":
            return "EXIT"
        if self.cellType == "ENTR":
            return "ENTR"

# Grid class : Basically a dictionary of cells with some useful functions
class Grid:
    def __init__(self):
        self.grid = {}
        self.width = 0
        self.height = 0
        self.entrances = {} # dict of (entranceID, cell) objects
        self.exits = {}  # dict of cell objects
        self.goals = {}  # dict of cell objects 
        self.parkingSpotList = [] # list of cell objects
        self.availableParkingSpotID = 0

    # Builds a grid from a text file
    def read_from_file(self, infile):
        # Reading from file
        f = open(infile, 'r')
        rawGrid = []

        for line in f:
            cellList = [cell_str.strip() for cell_str in line.split(',')]
            rawGrid.append(cellList)

        f.close()

        # Building the grid dictionary
        # x is the row
        # y is the coloumn
        x = 0
        for row in rawGrid:
            y = 0
            for cell in row:
                newCell = Cell((x,y), None)

                # wall
                if cell[0] == 'w':
                    newCell.cellType = "WALL"
                    self.grid[(x,y)] = newCell
                # road
                elif cell[0] == 'r':    # is road
                    newCell.cellType = "ROAD"
                    newCell.neighbors = []

                    for idx in range(1,len(cell)):
                        direction = cell[idx]
                        if direction == 'u':
                            newCell.up = True
                        if direction == 'd':
                            newCell.down = True
                        if direction == 'l':
                            newCell.left = True
                        if direction == 'r':
                            newCell.right = True
                # parking spot 
                elif cell[0] == 'p' or cell[0] == 'f' or cell[0] == 'h' or cell[0] == 'a':    # is parking spot
                    newCell.cellType = "PARK"
                    newCell.idNum = self.availableParkingSpotID
                    self.availableParkingSpotID += 1
                    newCell.neighbors = []

                    if cell[0] == 'p':  # is empty
                        newCell.occupied = False
                    if cell[0] == 'f':  # is occupied
                        newCell.occupied = True
                    if cell[0] == 'h':  # is handicapped spot
                        newCell.occupied = False
                    if cell[0] == 'a':  # is occupied handicapped spot
                        newCell.occupied = True

                    for idx in range(1,len(cell)):
                        direction = cell[idx]
                        if direction == 'u':
                            newCell.up = True
                        if direction == 'd':
                            newCell.down = True
                        if direction == 'l':
                            newCell.left = True
                        if direction == 'r':
                            newCell.right = True
                # goal
                elif cell[0] == 'g':
                    newCell.cellType = "GOAL"
                    if (len(cell) > 1) and isInt(cell[1]):
                        newCell.idNum = int(cell[1])
                    else:
                        print "error: a goal has no id number"
                # exit
                elif cell[0] == 'x':
                    newCell.cellType = "EXIT"
                    if (len(cell) > 1) and isInt(cell[1]):
                        newCell.idNum = int(cell[1])
                    else:
                        print "error: an exit has no id number"
                #entrance
                elif cell[0] == 'e':
                    newCell.cellType = "ENTR"
                    newCell.neighbors = []
                    if (len(cell) > 1) and isInt(cell[1]):
                        newCell.idNum = int(cell[1])
                    else:
                        print "error: an entrance has no id number"

                    for idx in range(2,len(cell)):
                        direction = cell[idx]
                        if direction == 'u':
                            newCell.up = True
                        if direction == 'd':
                            newCell.down = True
                        if direction == 'l':
                            newCell.left = True
                        if direction == 'r':
                            newCell.right = True
                            
                # write the new cell to data structure
                self.grid[(x,y)] = copy.deepcopy(newCell)
                y += 1
            x += 1
            
        # Setting height and width of the grid
        self.height = x
        self.width = y
       
        # Loop through the grid and extract additional information
        for x in range(0,self.height):
            for y in range(0, self.width):
                cell = self.grid[(x,y)]
                
                # appending speacial cells to their respective list
                if cell.cellType == "WALL": # nothing to extract
                    continue
                elif cell.cellType == "PARK":  # If parking spot append to list
                    self.parkingSpotList.append(cell)
                elif cell.cellType == "GOAL":
                    self.goals[cell.idNum] = cell
                elif cell.cellType == "ENTR":
                    self.entrances[cell.idNum] = cell
                elif cell.cellType == "EXIT":
                    self.exits[cell.idNum] = cell
 
                # connecting unconnected roads and parking spaces
                if cell.cellType == 'ROAD' or cell.cellType == 'GOAL':
                    if x > 0:
                        upcell = self.grid[(x-1,y)]
                        if upcell.cellType == 'PARK':
                            cell.newUp = True
                        elif not (cell.up or upcell.down) and (upcell.cellType == 'ROAD' or upcell.cellType == 'PARK' or upcell.cellType == 'GOAL'):
                            cell.newUp = True
                    if x < self.height - 1:
                        downcell = self.grid[(x+1,y)]
                        if downcell.cellType == 'PARK':
                            cell.newDown = True
                        elif not (cell.down or downcell.up) and (downcell.cellType == 'ROAD' or downcell.cellType == 'PARK' or downcell.cellType == 'GOAL'):
                            cell.newDown = True
                    if y > 0:
                        leftcell = self.grid[(x,y-1)]
                        if leftcell.cellType == 'PARK':
                            cell.newLeft = True
                        elif not (cell.left or leftcell.right) and (leftcell.cellType == 'ROAD' or leftcell.cellType == 'PARK' or leftcell.cellType == 'GOAL'):
                            cell.newLeft = True
                    if y < self.width - 1:
                        rightcell = self.grid[(x,y+1)]
                        if rightcell.cellType == 'PARK':
                            cell.newRight = True
                        if not (cell.right or rightcell.left) and (rightcell.cellType == 'ROAD' or rightcell.cellType == 'PARK' or rightcell.cellType == 'GOAL'):
                            cell.newRight = True
                    
                elif cell.cellType == 'PARK':
                    if x > 0:
                        upcell = self.grid[(x-1,y)]
                        if (upcell.cellType == 'ROAD'):
                            cell.newUp = True
                    if x < self.height - 1:
                        downcell = self.grid[(x+1,y)]
                        if (downcell.cellType == 'ROAD'):
                            cell.newDown = True
                    if y > 0:
                        leftcell = self.grid[(x,y-1)]
                        if (leftcell.cellType == 'ROAD'):
                            cell.newLeft = True
                    if y < self.width - 1:
                        rightcell = self.grid[(x,y+1)]
                        if (rightcell.cellType == 'ROAD'):
                            cell.newRight = True
                            
        # creating neighborList
        for x in range(0,self.height):
            for y in range(0, self.width):
                cell = self.grid[(x,y)]
                if cell.up or cell.newUp:
                    cell.up = True
                    cell.neighbors.append((x-1,y))
                if cell.down or cell.newDown:
                    cell.down = True
                    cell.neighbors.append((x+1,y))
                if cell.left or cell.newLeft:
                    cell.left = True
                    cell.neighbors.append((x,y-1))
                if cell.right or cell.newRight:
                    cell.right = True
                    cell.neighbors.append((x,y+1))
 
    def writeToFile(self,outfile):
        f = open(outfile, 'w')
        rawGrid = []

        grid = self.grid
        for x in range(0, self.height):
            for y in range(0, self.width):
                print 'x: ' + str(x) + ' y: ' + str(y)
                cell = grid[(x,y)]
                wstr = cell.cellType[0]

                if cell.cellType == 'PARK':
                    wstr = 'p'

                if cell.cellType == 'WALL':
                    wstr = 'w'

                if cell.cellType == 'ROAD':
                    wstr = 'r'

                if cell.cellType == 'ENTR':
                    wstr = 'e'

                if cell.cellType == 'EXIT':
                    wstr = 'x' + str(cell.idnum)

                if cell.up:
                    wstr += 'u'
                if cell.down:
                    wstr += 'd'
                if cell.left:
                    wstr += 'l'
                if cell.right:
                    wstr += 'r'

                if cell.cellType == 'GOAL':
                    wstr = 'g' + str(cell.idnum)

                f.write(wstr + ',')
            f.write('\n')

        f.write('!\n')
        
        f.close()
        return None

    def isExit(self, pos):
        for _, cell in self.exits.iteritems():
            print "debugging start"
            print pos
            print cell.pos
            print "debugging end"
            if cell.pos == pos:
                return True
        return False

    # returns a list of neighbors of all types
    # pos = (x,y) is a tuple
    def getNeighbors(self, pos):
        cell = self.grid[pos]
        print str(pos) + " neighbors: " + str(cell.neighbors)
        return cell.neighbors

    # returns a list of position of neighbors that are either road or parking spot
    # pos = (x,y) is a tuple
    def getNeighbors_road(self, pos, parkingSpotPos):
        neighbors_road = []
        cell = self.grid[pos]
        for npos in cell.neighbors:
            neighCell = self.grid[npos]
            #if (neighCell.cellType == "ROAD" or neighCell.cellType == "PARK" or neighCell.cellType == "EXIT"):
            if (neighCell.cellType == "ROAD" or neighCell.cellType == "EXIT" or neighCell.pos == parkingSpotPos):
                neighbors_road.append(npos)
        return neighbors_road

    # manhattan distance helper function
    def manhattanDist((x0,y0), (x1,y1)):
        return abs(x0 - x1) + abs(y0 - y1)

    # finds path from startPos to goalPos
    # returns path as a list of positions
    def findPathBFS(self, startPos, goalPos):
        q = Queue.Queue()
        visited = {}
        pathList = []

        q.put((startPos, None, 0))
        while not q.empty():
            (pos, parent, cost) = q.get()

            if pos == goalPos:
                while pos != startPos:
                    pathList.append(pos)
                    (pos, _) = visited[pos]
                return pathList
            
            cell = self.grid[pos]
            neighborList = self.getNeighbors_road(pos, goalPos)
            
            for nPos in neighborList:
                if nPos not in visited:
                    visited[nPos] = (pos, cost)
                    q.put((nPos, pos, cost+1))
                    
        print "error: no path found from " + str(startPos) + " to " + str(goalPos)
        return 1
    
    def findPathBFS_alternative(self, startPos, goalPos, forbiddenPos):
        q = Queue.Queue()
        visited = {}
        pathList = []

        q.put((startPos, None, 0))
        (pos, parent, cost) = q.get()

        # ignore occupied neighbor only at the first step
        if pos == goalPos:
            while pos != startPos:
                pathList.append(pos)
                (pos, _) = visited[pos]
            return pathList
        
        cell = self.grid[pos]
        neighborList = self.getNeighbors_road(pos, goalPos)
        
        for nPos in neighborList:
            if not self.grid[nPos].occupied:
                visited[nPos] = (pos, cost)
                q.put((nPos, pos, cost+1))
             
        while not q.empty():
            (pos, parent, cost) = q.get()

            if pos == goalPos:
                while pos != startPos:
                    pathList.append(pos)
                    (pos, _) = visited[pos]
                return pathList
            
            cell = self.grid[pos]
            neighborList = self.getNeighbors_road(pos, goalPos)
            
            for nPos in neighborList:
                if nPos not in visited:
                    visited[nPos] = (pos, cost)
                    q.put((nPos, pos, cost+1))
                    
        print "error: no path found from " + str(startPos) + " to " + str(goalPos)
        print "moving to any possible position"
        for nPos in self.getNeighbors_road(startPos, goalPos):
            if not self.grid[nPos].occupied:
                return [nPos]
        print "error: deadlock"
        return []
 
    def findPathBFS_to_exit(self, startPos, exitID):
        return self.findPathBFS(startPos, self.exits[exitID].pos)
