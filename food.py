import random
import math
import coordinate

class Food:
    
    #Constructor to a food object
    def __init__(self,image,sound,xSize,ySize,xBoundry,yBoundry): 
        self.sound = sound
        self.image = image
        self.xSize = xSize
        self.ySize = ySize
        self.coordinate = coordinate.Coordinate(math.ceil(random.randint(0, xBoundry - xSize) / float(xSize)) * xSize, math.ceil(random.randint(0, yBoundry - ySize) / float(ySize)) * ySize)
        print(f'Instantiated food coordinates: {self.coordinate}')