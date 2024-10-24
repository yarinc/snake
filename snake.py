import coordinate

class Snake: 
    direction = ""

    #Constructor to build new snake
    def __init__(self,color,xLocation,yLocation,xSize,ySize):
        self.coordinates = []
        self.color = color
        location = coordinate.Coordinate(xLocation,yLocation)
        print(f'Starting location: {location}')
        self.coordinates.append(location)
        self.xSize = xSize
        self.ySize = ySize
    
    #Method that check if the snake head hit the given coordiate
    def compareHeadCoordinate(self, coordinate) -> bool:
        if self.coordinates[0].compare(coordinate):
            return True
        return False
    
    #Method that check if the snake head and one of the body parts have collided
    def headInBody(self) -> bool:
        #We need to check only when the snake size is >=4 because there is no point to check prior to that
        if len(self.coordinates) > 3:
            for coor in range(1,len(self.coordinates)):
                if self.coordinates[coor].compare(self.coordinates[0]):
                    print("Snake's head hit the body.")
                    return True
        return False
    
    #Method to set the direction of the snake
    def changeDirection(self,direction):
        self.direction = direction
    
    #Method to move the snake up by removing the last object and set it as the new head
    def moveSnakeUp(self):
        firstPiece = self.coordinates[0]
        self.coordinates.pop()

        #Set the new head above the previous snake's head
        newPiece = coordinate.Coordinate(firstPiece.x,firstPiece.y - self.ySize)
        self.coordinates.insert(0,newPiece)

    #Method to move the snake down by removing the last object and set it as the new head
    def moveSnakeDown(self):
        firstPiece = self.coordinates[0]
        self.coordinates.pop()

        #Set the new head below the previous snake's head
        newPiece = coordinate.Coordinate(firstPiece.x,firstPiece.y + self.ySize)
        self.coordinates.insert(0,newPiece)

    #Method to move the snake right by removing the last object and set it as the new head
    def moveSnakeRight(self):
        firstPiece = self.coordinates[0]
        self.coordinates.pop()

        #Set the snake's new head to the right of the previous snake's head
        newPiece = coordinate.Coordinate(firstPiece.x + self.xSize,firstPiece.y)
        self.coordinates.insert(0,newPiece)

    #Method to move the snake to the left by removing the last object and set it as the new head
    def moveSnakeLeft(self):
        firstPiece = self.coordinates[0]
        self.coordinates.pop()

        #Set the snake's new head to the left of the previous snake's head
        newPiece = coordinate.Coordinate(firstPiece.x - self.xSize,firstPiece.y)
        self.coordinates.insert(0,newPiece)

    #Method to expand the snake by appending a another item to the coordinate list
    def expandSnake(self):
        self.coordinates.append(self.coordinates[0])
    
    #Method to set a new direction of the snake. Return true if direction change, otherwise return false
    #We need to make sure we do not change direction to the opposite direction as it's not allowed
    def canChangeDirection(self,newDirection):
        match newDirection:
            case "up":
                if len(self.coordinates) > 1:
                    if self.coordinates[0].y > self.coordinates[1].y:
                        print("direction not allowed in current state!")
                        return False
            case "down":
                if len(self.coordinates) > 1:
                    if self.coordinates[0].y < self.coordinates[1].y:
                        print("direction not allowed in current state!")
                        return False
            case "right":
                if len(self.coordinates) > 1:
                    if self.coordinates[0].x < self.coordinates[1].x:
                        print("direction not allowed in current state!")
                        return False
            case "left":
                if len(self.coordinates) > 1:
                    if self.coordinates[0].x > self.coordinates[1].x:
                        print("direction not allowed in current state!")
                        return False
        return True