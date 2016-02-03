import copy
import Queue

class Cell:
    def __init__(self, (x, y), cellType):
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.cellType = None
        self.neighbors = None
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.occupied = False
        self.goalName = None

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

    # Builds a grid from a text file
    def readFromFile(self, infile):
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

                if cell[0] == 'w':  # is a wall
                    newCell.cellType = "WALL"
                    self.grid[(x,y)] = newCell

                elif cell[0] == 'r':    # is road
                    newCell.cellType = "ROAD"
                    newCell.neighbors = []

                    for idx in range(1,len(cell)):
                        direction = cell[idx]
                        if direction == 'u':
                            newCell.up = True
                            newCell.neighbors.append((x-1,y))
                        if direction == 'd':
                            newCell.down = True
                            newCell.neighbors.append((x+1,y))
                        if direction == 'l':
                            newCell.left = True
                            newCell.neighbors.append((x,y-1))
                        if direction == 'r':
                            newCell.right = True
                            newCell.neighbors.append((x,y+1))

                elif cell[0] == 'p':    # is parking spot
                    newCell.cellType = "PARK"
                    newCell.neighbors = []

                    if cell[1] == 'e':  # is empty
                        newCell.occupied = False
                    if cell[1] == 'f':  # is occupied
                        newCell.occupied = True

                    for idx in range(2,len(cell)):
                        direction = cell[idx]
                        if direction == 'u':
                            newCell.up = True
                            newCell.neighbors.append((x-1,y))
                        if direction == 'd':
                            newCell.down = True
                            newCell.neighbors.append((x+1,y))
                        if direction == 'l':
                            newCell.left = True
                            newCell.neighbors.append((x,y-1))
                        if direction == 'r':
                            newCell.right = True
                            newCell.neighbors.append((x,y+1))

                elif cell[0] == 'g':    # is goal
                    newCell.cellType = "GOAL"
                    newCell.goalName = copy.deepcopy(cell[1])

                elif cell == 'exit':    # is exit
                    newCell.cellType = "EXIT"

                elif cell == 'entr':    # is entrance
                    newCell.cellType = "ENTR"

                self.grid[(x,y)] = copy.deepcopy(newCell)
                y += 1
            x += 1

    # Get a list of valid, non occupied neighbors
    # if no neighbor found, returns None
    def getNeighbors(self, (x,y)):
        cell = self.grid[(x,y)]

        if cell.neighbors is None:
            return None

        neighbors = []
        for pos in cell.neighbors:
            if not self.grid[pos].occupied:
                neighbors.append(pos)

        if len(neighbors):
            return neighbors

        return None

    def manhattanDist((x0,y0), (x1,y1)):
        return abs(x0 - x1) + abs(y0 - y1)

    def findPathBFS(self, startPos, goalPos):
        q = Queue.Queue()
        visited = {}
        pathList = []

        q.put((startPos, None, 0))
        while not q.empty():
            (pos, parent, cost) = q.get()
            #print pos
            # If goal found.
            if pos == goalPos:
                while pos != startPos:
                    pathList.append(pos)
                    (pos, _) = visited[pos]

                return pathList

            cell = self.grid[pos]
            neighborList = self.getNeighbors(pos)

            if neighborList is None:
                continue

            for nPos in neighborList:
                if nPos not in visited:
                    visited[nPos] = (pos, cost)
                    q.put((nPos, pos, cost+1))

        return 1


    """
    # Finds best path from startPos to goal
    def findPath(self, startPos, goalPos):
        pq = Queue.PriorityQueue()
        pq.put(startPos)

        while not pq.empty():
            (val, pos) = pq.get()

            # Goal popped, so end the search
            if pos == goalPos:
                return

            cell = self.grid[pos]
            neighborList = self.getNeighbors(pos)

            # No neighbor, dead end, continue
            if neighborList is None:
                continue

            for nPos in neighborList:
                # Calculate the Heuristic value
                hVal = manhattanDist(nPos, goalPos)
    """
