#!/usr/bin/python

class Space:

    spaceTypes = ["w", "p", "t"]
    orientedSpaceTypes = ["c", "r", "e", "x"]

    def __init__(self, spaceType, orientation = None):
        if "-" in spaceType:
            spaceType, orientation = spaceType.split("-")
            orientation = Orientation(orientation)
        if spaceType not in Space.spaceTypes + Space.orientedSpaceTypes:
            raise Exception('Invalid space')
        if spaceType in Space.orientedSpaceTypes and orientation == None:
            raise Exception('Space must be oriented')
        self.spaceType = spaceType
        self.orientation = orientation

    def getOrientation(self):
        return self.orientation

    def isOriented(self):
        return self.orientation != None
    def isEntrance(self):
        return self.spaceType == "e" #entrance
    def isExit(self):
        return self.spaceType == "x" #exit
    def isWall(self):
        return self.spaceType == "w" #wall
    def isParkingSpot(self):
        return self.spaceType == "p" #parking spot
    def isCar(self):
        return self.spaceType == "c" #car
    def isRaod(self):
        return self.spaceType == "r" #road

class Orientation:

    orientations = ["u", "d", "l", "r"]

    def __init__(self, orientation):
        for direction in orientation:
            if direction not in Orientation.orientations:
                raise Exception('Invalid orientation')
        self.orientation = orientation

    def isUp(self):
        return "u" in self.orientation
    def isDown(self):
        return "d" in self.orientation
    def isLeft(self):
        return "l" in self.orientation
    def isRight(self):
        return "r" in self.orientation

if __name__ == "__main__":

    parkingSpot = Space("p")
    assert(not parkingSpot.isOriented())
    assert(not parkingSpot.isEntrance())
    assert(parkingSpot.isParkingSpot())

    try:
        bad = Space("bad")
        assert(False)
    except Exception:
        assert(True)

    car = Space("c-u")
    assert(car.isOriented())
    assert(car.getOrientation().isUp())
    assert(not car.getOrientation().isDown())

    road = Space("r-ud")
    assert(road.isOriented())
    assert(road.getOrientation().isUp())
    assert(road.getOrientation().isDown())

    try:
        bad = Orientation("bad")
        assert(False)
    except Exception:
        assert(True)
