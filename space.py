#!/usr/bin/python

class Space:

    spaceTypes = ["entrance", "exit", "wall", "parkingSpot"]
    orientedSpaceTypes = ["car", "road"]

    def __init__(self, spaceType, orientation=None):
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
        return self.spaceType == "entrance"
    def isExit(self):
        return self.spaceType == "exit"
    def isWall(self):
        return self.spaceType == "wall"
    def isParkingSpot(self):
        return self.spaceType == "parkingSpot"
    def isCar(self):
        return self.spaceType == "car"
    def isRaod(self):
        return self.spaceType == "road"

class Orientation:

    orientations = ["up", "down", "left", "right"]

    def __init__(self, orientation):
        if type(orientation) == type(""):
            orientation = [orientation]
        for direction in orientation:
            if direction not in Orientation.orientations:
                raise Exception('Invalid orientation')
        self.orientation = orientation

    def isUp(self):
        return "up" in self.orientation
    def isDown(self):
        return "down" in self.orientation
    def isLeft(self):
        return "left" in self.orientation
    def isRight(self):
        return "right" in self.orientation

if __name__ == "__main__":

    entrance = Space("entrance")
    assert(not entrance.isOriented())
    assert(entrance.isEntrance())

    exit = Space("exit")
    assert(not exit.isOriented())
    assert(exit.isExit())

    try:
        bad = Space("bad")
        assert(False)
    except Exception:
        assert(True)

    up = Orientation("up")
    car = Space("car", up)
    assert(car.isOriented())
    assert(car.getOrientation().isUp())
    assert(not car.getOrientation().isDown())

    upDown = Orientation(["up", "down"])
    road = Space("road", upDown)
    assert(road.isOriented())
    assert(road.getOrientation().isUp())
    assert(road.getOrientation().isDown())

    try:
        bad = Orientation("bad")
        assert(False)
    except Exception:
        assert(True)
