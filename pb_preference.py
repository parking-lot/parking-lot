import heapq as hq

class Preference:
    def __init__(self):
        self.grid = None
        self.pq = None
        self.psList = None #parking spot list
        self.gList = None #goal list
        self.exitList = None #exit list

    def loadGrid(self, grid):
        self.grid = grid
        self.pq = []
        self.psList = self.grid.parkingSpotList()
        self.gList = self.grid.goalList()

    def manhattan_dist(self, (x0,y0), (x1,y1)):
        return abs(x0 - x1) + abs(y0 - y1)

    def createPriorityList(self):
        goalPos = self.gList[0]
        for ps in self.psList:
            compVal = self.manhattan_dist(ps, goalPos)
            hq.heappush(self.pq, (compVal, ps))

        return None

    # returns tuple (distance, (x, y))
    def getParkingSpot(self):
        return hq.heappop(self.pq)

# Closest to goal
class Preference_00(Preference):
    def hVal(self, (x0,y0), (x1,y1)):
        return abs(x0 - x1) + abs(y0 - y1)

    def createPriorityList(self):
        goalPos = self.gList[0]
        for ps in self.psList:
            compVal = self.hVal(ps, goalPos)
            hq.heappush(self.pq, (compVal, ps))
        return None

# Closest to goal (temporal)
class Preference_01(Preference):
    def pathLength(self, (x0, y0), (x1, y1)):
        temp_list = self.grid.findPathBFS((x0, y0), (x1, y1))
        return len(temp_list)

    # currently supports only 1 entrance
    def createPriorityList(self, entrancePos):
        walk_weight = 1.5 # Larger value is larger penalty
        park_weight = 1.1 # Larger value is larger penalty
        goalPos = self.gList[0]
        for psPos in self.psList:
            compVal = (walk_weight * self.manhattan_dist(psPos, goalPos)) + (park_weight * self.pathLength(entrancePos, psPos))
            hq.heappush(self.pq, (compVal, psPos))
        return None

# Fastest exit (temporal)
class Preference_02(Preference):
    def loadGrid(self, grid):
        self.grid = grid
        self.pq = []
        self.psList = self.grid.parkingSpotList()
        self.gList = self.grid.goalList()

    def pathLength(self, (x0, y0), (x1, y1)):
        temp_list = self.grid.findPathBFS((x0, y0), (x1, y1))
        return len(temp_list)

    def createPriorityList(self, entrancePos):
        self.exitList = self.grid.exitList()
        walk_weight = 1.0 # Larger value is larger penalty
        exit_weight = 1.1 # Larger value is larger penalty
        goalPos = self.gList[0]
        exitPos = self.exitList[0]
        for psPos in self.psList:
            compVal = (walk_weight * self.manhattan_dist(psPos, goalPos)) + (exit_weight * self.pathLength(psPos, exitPos))
            hq.heappush(self.pq, (compVal, psPos))
        return None
