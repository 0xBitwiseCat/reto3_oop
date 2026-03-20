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

class Numerical:
    error_diff = 1e-8
    p0 = Point(0.0,0.0)

#- define Line class
class Line(Numerical):
    def __init__(self, start: Point, end: Point):
        if start.compute_distance(end) < self.error_diff:
            start = self.p0
            end = Point(1,1)
        self.start = start
        self.end = end
        self.length = self.compute_length()
        self.slope = self.compute_slope()

    #- compute slope from start and end in degrees
    def compute_slope(self) -> float:
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y

        #- rad to degrees in order to accomplish requirement
        #? atan2 handles zero-division error
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
        if abs(self.start.y - self.end.y) < self.error_diff:
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
        
        #- if the line is a vertical line
        if abs(self.start.x - self.end.x) < self.error_diff:
            return Point(0.0, self.start.y)
            
        #- x(t) = x0 + t(x1 - x0). t when x=0.
        t = -self.start.x / (self.end.x - self.start.x)
        intercept_y = self.start.y + t * (self.end.y - self.start.y)
        return Point(0.0, intercept_y)

    #++ optional but why not 
    def discretize_line(self, n: int = 2):
        if n <= 1:
            return None
        if n == 2:
            return [self.start, self.end]
        
        #++ so basically this function is numpy.linspace
        #* I use lambda just for fun and make it fashioned
        fx = lambda i: self.start.x + ((i-1)/(n-1))*(self.end.x - self.start.x)
        fy = lambda i: self.start.y + ((i-1)/(n-1))*(self.end.y - self.start.y)

        dl = []

        #++ evaluate fx, fy por each possible point to get coordenates
        for j in range(1,n+1,1):
            dl.append(Point(fx(j), fy(j)))

        return dl

    def dot(self, l0: Line):
        dx = (self.end.x - self.start.x)*(l0.end.x - l0.start.x)
        dy = (self.end.y - self.start.y)*(l0.end.y - l0.start.y)
        return dx + dy

    def is_connected(self, l0: Line):
        ss = self.start.compute_distance(l0.start) < self.error_diff
        se = self.start.compute_distance(l0.end) < self.error_diff
        es = self.end.compute_distance(l0.start) < self.error_diff
        ee = self.end.compute_distance(l0.end) < self.error_diff
        return ss or se or es or ee
    
    def __repr__(self):
        return f"x in [{self.start.x}, {self.end.x}] and y in [{self.start.y}, {self.end.y}]"

class Rectangle(Numerical):
    """
    Creates a Rectangle
    config must be the following structure:
    {
        method (int): 1 <= m <= 4
        width (float?): 0 < w, only if method is 1 or 2
        height (float?): 0 < h, only if method is 1 or 2
        center (Point?): only if method is 2
        bottom-left-corner (Point?): only if method is 1 or 3
        bottom-right-corner (Point?): only if method is 3 
        upper-left-corner (Point?): only if method is 3
        upper-right-corner (Point?): only if method is 3
        lines ({
            left Line 
            right Line 
            up Line
            down Line
        }): only if method is 4
    }
    """
    def __init__(self, config: dict):
        hl = "Creating a default rectangle..."
        m = config.get("method")
        if m and m in [1,2,3,4]:
            #? Method 1: Bottom-left corner(Point) + width and height
            if m == 1:
                #++ search for dimensions
                blc = config.get("bottom-left-corner")
                w = config.get("width", 1)
                h = config.get("height", 1) 

                if w <= 0 or h <= 0 or not isinstance(blc, Point):
                    #! create an unitary square at (0,0)
                    self.width = 1
                    self.height = 1
                    self.center = self.p0
                    print("Warning: dimensions are not valid.", hl)
                    return

                self.width = w
                self.height = h
                self.center = Point(blc.x + w/2, blc.y + h/2)
            
            #? Method 2: Center(Point) + width and height
            elif m == 2:
                c = config.get("center")
                w = config.get("width", 1)
                h = config.get("height", 1) 

                if w <= 0 or h <= 0 or not isinstance(c, Point):
                    #! create an unitary square at (0,0)
                    self.width = 1
                    self.height = 1
                    self.center = self.p0
                    print("Warning: dimensions are not valid.", hl)
                    return

                self.width = w
                self.height = h
                self.center = c
            
            #? Method 3: Two opposite corners (Points) e.g. Bottom-left and Upper-right
            elif m == 3:
                blc = config.get("bottom-left-corner")
                brc = config.get("bottom-right-corner")
                ulc = config.get("upper-left-corner")
                urc = config.get("upper-right-corner")

                if isinstance(blc, Point) and isinstance(urc, Point):
                    #++ creating a rectangle using two opposite corners
                    w = abs(blc.x - urc.x)
                    h = abs(blc.y - urc.y)

                    if w <= 0 or h <= 0:
                        #! create an unitary square at (0,0)
                        self.width = 1
                        self.height = 1
                        self.center = self.p0
                        print("Warning: dimensions are not valid.", hl)
                        return

                    self.width = w
                    self.height = h
                    self.center = Point((blc.x + urc.x)/2, (blc.y + urc.y)/2)

                elif isinstance(brc, Point) and isinstance(ulc, Point):
                    #++ creating a rectangle using two opposite corners
                    #++ creating a rectangle using two opposite corners
                    w = abs(brc.x - ulc.x)
                    h = abs(brc.y - ulc.y)

                    if w <= 0 or h <= 0:
                        #! create an unitary square at (0,0)
                        self.width = 1
                        self.height = 1
                        self.center = self.p0
                        print("Warning: dimensions are not valid.", hl)
                        return

                    self.width = w
                    self.height = h
                    self.center = Point((brc.x + ulc.x)/2, (brc.y + ulc.y)/2)
                else:
                    #! another combination is not valid
                    self.width = 1
                    self.height = 1
                    self.center = self.p0
                    print("Warning: given points does not satisfy requirements.", hl)
                    return
            
            #!! New: initialization using 4 Lines 
            #!! (composition at its best, a rectangle is compose of 4 lines).
            elif m == 4:
                ls = config.get("lines", {})
                if len(ls.keys()) != 4:
                    self.width = 1
                    self.height = 1
                    self.center = self.p0
                    print("Warning: given lines are not enough.", hl)
                    return

                left = ls.get("left")
                right = ls.get("right")
                up = ls.get("up") 
                down = ls.get("down") 

                if not isinstance(left, Line) or not isinstance(right, Line) or not isinstance(up, Line) or not isinstance(down, Line):
                    self.width = 1
                    self.height = 1
                    self.center = self.p0
                    print("Warning: given lines does not satisfy requirements.", hl)
                    return 
                
                #++ validate if the lines are ortogonal
                lu = left.dot(up)
                ld = left.dot(down)
                ru = right.dot(up)
                rd = right.dot(down)

                #! if all lines are ortogonal then all dot products are 0
                if any([abs(lu) > self.error_diff, abs(ld) > self.error_diff, abs(ru) > self.error_diff, abs(rd) > self.error_diff]):
                    self.width = 1
                    self.height = 1
                    self.center = self.p0
                    print("Warning: given lines does not satisfy requirements.", hl)
                    return

                #++ validate if left and right are "face-to-face" (idk how to describe that)
                #* if the user describes the lines in the same way then vx defines diagonal 
                #* but if the user describes the lines in a opposite way then vx should be the width 
                vx0 = left.start.compute_distance(right.end)
                vx1 = left.end.compute_distance(right.start)

                #* if there is a significant difference between 
                #* vx0 and vx1 then they are not "face-to face"
                if abs(vx0 - vx1) > self.error_diff:
                    self.width = 1
                    self.height = 1
                    self.center = self.p0
                    print("Warning: given lines does not satisfy requirements.", hl)
                    return

                #++ the same but for up and down
                vy0 = up.start.compute_distance(down.end)
                vy1 = up.end.compute_distance(down.start)

                if abs(vy0 - vy1) > self.error_diff:
                    self.width = 1
                    self.height = 1
                    self.center = self.p0
                    print("Warning: given lines does not satisfy requirements.", hl)
                    return

                #++ if all lines are "face-to-face" it means that are parallel with their opposite
                #++ but it does not imply that the rectangle is well-formed
                #++ It is mandatory to garantee that there is a 
                #++ common-point between two ortogonal lines

                #* there is no shared point between left and up
                if not left.is_connected(up): 
                    self.width = 1
                    self.height = 1
                    self.center = self.p0
                    print("Warning: given lines does not satisfy requirements.", hl)
                    return
    
                #* there is no shared point between left and down
                if not left.is_connected(down): 
                    self.width = 1
                    self.height = 1
                    self.center = self.p0
                    print("Warning: given lines does not satisfy requirements.", hl)
                    return

                #++ calculate distances between right and up
                #* there is no shared point between right and up
                if not right.is_connected(up):
                    self.width = 1
                    self.height = 1
                    self.center = self.p0
                    print("Warning: given lines does not satisfy requirements.", hl)
                    return

                #* there is no shared point between right and down
                if not right.is_connected(down):
                    self.width = 1
                    self.height = 1
                    self.center = self.p0
                    print("Warning: given lines does not satisfy requirements.", hl)
                    return

                #* after all of these validations then it is possible to affirm that the lines build a rectangle
                self.width = down.compute_length() #? there is no reason to use down, up is valid too
                self.height = left.compute_length() #? there is no reason to use left, right is valid too
                
                #++ using left to determinate which point is the "bottom-left-corner" in order to
                #++ calculate the center as (x0 + w/2, y0 + h/2)
                if left.start.compute_distance(self.p0) < left.end.compute_distance(self.p0):
                    #* start  is the "bottom-left-corner"
                    #? is it possible to use up or right to get the diagonal
                    ss = right.start.compute_distance(left.start)
                    es = right.end.compute_distance(left.start)
                    pf = right.start if ss > es else right.end

                    self.center = Point((left.start.x + pf.x)/2, (left.start.y + pf.y)/2)
                else:
                    #* end  is the "bottom-left-corner"
                    #? is it possible to use up or right to get the diagonal
                    ss = right.start.compute_distance(left.end)
                    es = right.end.compute_distance(left.end)
                    pf = right.start if ss > es else right.end

                    self.center = Point((left.end.x + pf.x)/2, (left.end.y + pf.y)/2)
        else:
            #++ create an unitary square at (0,0)
            self.width = 1
            self.height = 1
            self.center = self.p0
            print("Warning: config does not provide a valid method.", hl)
            return

    #! 'cause all rectangles are rectangles (obviously)
    #! there is no needed to keep the rotation so
    #! all calculations assume that the rectangle was transformed
    #! to 0 degrees of rotation
    #! rotation is irrelevant 
    def compute_area(self):
        return self.width*self.height
    
    def compute_perimeter(self):
        return self.width*2 + self.height*2

    def compute_interference_point(self, px: Point):
        # Calculate the horizontal and vertical distance from the center
        diff_x = abs(px.x - self.center.x)
        diff_y = abs(px.y - self.center.y)
    
        # The point is inside only if it is within half-width AND half-height
        return diff_x <= self.width/2 and diff_y <= self.height/2
    
    def __repr__(self):
        return f"Rectangle {self.width} x {self.height} centered by {self.center}"

# unit test
l1 = Line(Point(1,1), Point(-1,-1))
print(l1.compute_horizontal_cross()) # (0,0)
print(l1.compute_vertical_cross()) # (0,0)
print(l1.discretize_line(6))

l2 = Line(Point(1,1), Point(3,1))
print(l2.compute_horizontal_cross()) # None
print(l2.compute_vertical_cross()) # None


#! AI unit test 'cause im exhausted already
def test_rectangle_method_1():
    # Setup: 2x2 Square starting at (0,0)
    config = {
        "method": 1,
        "bottom-left-corner": Point(0, 0),
        "width": 2,
        "height": 2
    }
    rect = Rectangle(config)
    
    # Validation
    print(f"Test 1 - Area: {rect.compute_area()} (Expected: 4)")
    print(f"Test 1 - Perimeter: {rect.compute_perimeter()} (Expected: 8)")
    
    # Interference check: Point (1,1) is exactly in the center
    p_inside = Point(1, 1)
    print(f"Test 1 - Interference (1,1): {rect.compute_interference_point(p_inside)} (Expected: True)")

test_rectangle_method_1()

def test_rectangle_method_3():
    # Setup: Rectangle from (1,1) to (5,4)
    # Width = 4, Height = 3
    config = {
        "method": 3,
        "bottom-left-corner": Point(1, 1),
        "upper-right-corner": Point(5, 4)
    }
    rect = Rectangle(config)
    
    # Validation
    print(f"Test 2 - Area: {rect.compute_area()} (Expected: 12)")
    print(f"Test 2 - Perimeter: {rect.compute_perimeter()} (Expected: 14)")
    
    # Interference check: Point (10,10) is far outside
    p_outside = Point(10, 10)
    print(f"Test 2 - Interference (10,10): {rect.compute_interference_point(p_outside)} (Expected: False)")

test_rectangle_method_3()

def test_rectangle_method_4():
    # Setup: Creating 4 lines for a 10x5 rectangle
    l_down = Line(Point(0,0), Point(10,0))
    l_up = Line(Point(0,5), Point(10,5))
    l_left = Line(Point(0,0), Point(0,5))
    l_right = Line(Point(10,0), Point(10,5))
    
    config = {
        "method": 4,
        "lines": {
            "down": l_down,
            "up": l_up,
            "left": l_left,
            "right": l_right
        }
    }
    rect = Rectangle(config)
    
    # Validation
    print(f"Test 3 - Area: {rect.compute_area()} (Expected: 50)")
    
    # Interference check: Point on the edge (0,2.5) should be True
    p_edge = Point(0, 2.5)
    print(f"Test 3 - Interference (0,2.5): {rect.compute_interference_point(p_edge)} (Expected: True)")

test_rectangle_method_4()

def test_rectangle_output():
    config = {
        "method": 1,
        "bottom-left-corner": Point(0, 0),
        "width": 10,
        "height": 5
    }
    rect = Rectangle(config)
    
    # This will now use your new __repr__
    print(rect) 
    # Output: Rectangle 10 x 5 centered by (x: 5.0, y: 2.5)

    # Testing your new calculations
    print(f"Area: {rect.compute_area()}")
    print(f"Perimeter: {rect.compute_perimeter()}")
    
    # Interference check with a random point
    random_p = Point(2, 2)
    print(f"Is {random_p} inside? {rect.compute_interference_point(random_p)}")

test_rectangle_output()
