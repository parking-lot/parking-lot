class Car:
    def __init__(self, pos, time_in, time_staying, pref):
        self.time_in = time_in
        self.time_staying = time_staying
        self.pref = pref
        self.pos = pos
        self.parkPos = None
        self.pathList = []

    def setGoal(self, parkPos):
        self.parkPos = parkPos

    # load in car info from file
    def readFromFile(self, infile):
        # Reading from file
        f = open(infile, 'r')
        rawGrid = []

        for line in f:
            cellList = [cell_str.strip() for cell_str in line.split(',')]
            rawGrid.append(cellList)

        f.close()
