"""
- length, slope, start, end: Instance attributes, two of 
- them being points (so a line is composed at least of two points).
- compute_length(): should return the line's length
- compute_slope(): should return the slope of the line from tje horizontal in deg.
- compute_horizontal_cross(): should return if exists the intersection with x-axis
- compute_vertical_cross(): should return if exists the intersection with y-axis

++ Redefine the class Rectangle, adding a new method 
++ of initialization using 4 Lines (composition at its best, 
++ a rectangle is compose of 4 lines).

? Optional: Define a method called discretize_line() 
? that creates an array on n equally spaced points in 
? the line and assigned as a instance attribute.
"""


import math

#* Define point as base class
class Point:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def move(self, new_x: float, new_y: float):
        self.x = new_x
        self.y = new_y

    def reset(self):
        self.x = 0
        self.y = 0

    def compute_distance(self, point: "Point") -> float:
        return ((self.x - point.x)**2 + (self.y - point.y)**2)**0.5

    def __repr__(self):
        return f"(x: {self.x}, y: {self.y})"

#- define Line class
class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
        self.length = self.compute_length()
        self.slope = self.compute_slope()

    #- compute slope from start and end in degrees
    def compute_slope(self) -> float:
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        #- rad to degrees in order to accomplish requirement
        angle_rad = math.atan2(dy, dx)
        return round(math.degrees(angle_rad), 2)

    #- use the Point instance param to calculate length 
    def compute_length(self) -> float:
        return self.start.compute_distance(self.end)

    #- checks if y = 0 is in the line
    def intersects_x_axis(self) -> bool:
        #-if x0 or x1 is 0 or x0 and x1 has opposite sign
        return self.start.y * self.end.y <= 0

    def compute_horizontal_cross(self) -> Point | None:
        #- verify all cases
        if not self.intersects_x_axis():
            return None
        
        #- if the line is a horizontal line
        if self.start.y == self.end.y:
            return Point(self.start.x, 0.0)
        
        #- y(t) = y0 + t(y1 - y0). t when y=0.
        t = -self.start.y / (self.end.y - self.start.y)
        intercept_x = self.start.x + t * (self.end.x - self.start.x)
        return Point(intercept_x, 0.0)

    def intersects_y_axis(self) -> bool:
        #-if y0 or y1 is 0 or y0 and y1 has opposite sign
        return self.start.x * self.end.x <= 0

    def compute_vertical_cross(self) -> Point | None:
        #- verify all cases
        if not self.intersects_y_axis():
            return None
        
        #-if the line is a vertical line
        if self.start.x == self.end.x:
            return Point(0.0, self.start.y)
            
        #-x(t) = x0 + t(x1 - x0). t when x=0.
        t = -self.start.x / (self.end.x - self.start.x)
        intercept_y = self.start.y + t * (self.end.y - self.start.y)
        return Point(0.0, intercept_y)


# unit test
l1 = Line(Point(1,1), Point(-1,-1))
print(l1.compute_horizontal_cross()) # (0,0)
print(l1.compute_vertical_cross()) # (0,0)

l2 = Line(Point(1,1), Point(3,1))
print(l2.compute_horizontal_cross()) # None
print(l2.compute_vertical_cross()) # None
