from pb_grid import *


testMap = Grid()
testMap.readFromFile("test_map_02.txt")

# Debug Print
for x in range(0,10):
    for y in range(0,10):
        print (x,y)
        print testMap.grid[(x,y)]

print testMap.getNeighbors((1,1))
print testMap.getNeighbors((2,8))

print testMap.findPathBFS((8,1),(2,7))
print testMap.findPathBFS((8,1),(2,2))



