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
