class Coordinate:
    
    #Constructor to a coordinate object
    def __init__(self, x, y):
        self.x = x
        self.y = y
    #Method to stringify the coordinate
    def __str__(self) -> str:
        return f'({self.x},{self.y})'
    
    #Method to compare two coordinates. Return true if match, otherwise return false
    def compare(self,coordinate) -> bool:
        if self.x == coordinate.x and self.y == coordinate.y:
            return True
        return False