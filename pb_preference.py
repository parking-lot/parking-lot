"""
Test Preference : Closest to Goal
"""
import heapq as hq
#import pb_grid
#import copy

class Cell:
    def __init__(self, key, val):
        self.key = key
        self.val = val

    def __lt__(self, other):
        return self.intAttribute < other.intAttribute

class Preference:
    def __init__(self):
        self.grid = None
        self.pq = None

    def loadGrid(self, grid):
        self.grid = grid

    def hVal(self, (x0,y0), (x1,y1)):
        return abs(x0 - x1) + abs(y0 - y1)

    def createPriorityList(self):
        print self.grid
        self.pq = []

        psList = self.grid.parkingSpotList()
        gList = self.grid.goalList()
        goalPos = gList[0]
        for ps in psList:
            compVal = self.hVal(ps, goalPos)
            hq.heappush(self.pq, (compVal, ps))

        #print hq.heappop(self.pq)
        #print hq.heappop(self.pq)
        #print hq.heappop(self.pq)
        #print hq.heappop(self.pq)
        #print hq.heappop(self.pq)
        #print hq.heappop(self.pq)
        #print hq.heappop(self.pq)
        #print hq.heappop(self.pq)
        #print hq.heappop(self.pq)
        #print hq.heappop(self.pq)
        #print hq.heappop(self.pq)
        #print hq.heappop(self.pq)
        #print hq.heappop(self.pq)
        #print hq.heappop(self.pq)
        #print hq.heappop(self.pq)
        #print hq.heappop(self.pq)

        return None

    # returns tuple (distance, (x, y))
    def getParkingSpot(self):
        return hq.heappop(self.pq)

