import heapq as hq

class Preference:
    def __init__(self, grid, goalCell, name):
        self.grid = grid
        self.pq = []
        self.goalCell = goalCell
        self.name = name + str(goalCell.idNum)

    def manhattan_dist(self, (x0,y0), (x1,y1)):
        return abs(x0 - x1) + abs(y0 - y1)

    def createPriorityList(self):
        goalPos = self.gList[0]
        for ps in self.psList:
            compVal = self.manhattan_dist(ps, goalPos)
            hq.heappush(self.pq, (compVal, ps))

        return None

    # returns tuple (distance to parking spot, (x, y))
    def getParkingLengthPos(self):
        psPos = hq.heappop(self.pq)
        return psPos

    def removeParkingSpot(self, pos):
        for (compVal, psPos) in self.pq:
            if psPos == pos:
                self.pq.remove((compVal, psPos))
                

# Closest to goal
class Pref_closest_to_goal(Preference):
    
    def hVal(self, (x0,y0), (x1,y1)):
        return abs(x0 - x1) + abs(y0 - y1)

    def createPriorityList(self):
        for parkSpot in self.grid.parkingSpotList:
            compVal = self.hVal(parkSpot.pos, self.goalCell.pos)
            hq.heappush(self.pq, (compVal, parkSpot.pos))
        return None

# Closest to goal (temporal)
class Pref_closest_to_goal_temporal(Preference):
    def __init__(self, grid, goalCell, name, walk_weight, park_weight):
        self.grid = grid
        self.pq = []
        self.goalCell = goalCell
        self.name = name + str(goalCell.idNum)
        self.walk_weight = walk_weight
        self.park_weight = park_weight
        
    def createPriorityList(self, currPos):
        self.walk_weight = 2.0 # Larger value is larger penalty
        self.park_weight = 1.0 # Larger value is larger penalty
        for psPos in self.grid.parkingSpotList:
            compVal = (self.walk_weight * self.manhattan_dist(psPos, goalPos)) + (self.park_weight * self.grid.getPathLength(currPos, psPos))
            hq.heappush(self.pq, (compVal, psPos))
        return None

# Fastest exit (temporal)
class Pref_fastest_to_exit_temporal(Preference):
    def pathLength(self, (x0, y0), (x1, y1)):
        temp_list = self.grid.findPathBFS((x0, y0), (x1, y1))
        return len(temp_list)

    def createPriorityList(self, entrancePos):
        self.exitList = self.grid.exitList()
        self.walk_weight = 1.0 # Larger value is larger penalty
        self.exit_weight = 2.0 # Larger value is larger penalty
        goalPos = self.gList[0]
        exitPos = self.exitList[0]
        for psPos in self.psList:
            compVal = (self.walk_weight * self.manhattan_dist(psPos, goalPos)) + (self.exit_weight * self.pathLength(psPos, exitPos))
            hq.heappush(self.pq, (compVal, psPos))
        return None
