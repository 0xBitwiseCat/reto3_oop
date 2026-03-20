# Reto 3

## Ejercicio de clase
1. Create class Line.

```mermaid
classDiagram
    class Line {
      +float length
      +float slope
      +Point start
      +Point end
      +__init__(self, start, end)
      +compute_length()
      +compute_slope()
      +compute_horizontal_cross()
      +compute_vertical_cross()
    }
```

- *length*, *slope*, start, end: Instance attributes, two of them being points (so a line is composed at least of two points).
- compute_length(): should return the line´s length
- compute_slope(): should return the slope of the line from tje horizontal in deg.
- compute_horizontal_cross(): should return if exists the intersection with x-axis
- compute_vertical_cross(): should return if exists the intersection with y-axis
1. Redefine the class Rectangle, adding a new method of initialization using 4 Lines (composition at its best, a rectangle is compose of 4 lines).
2. **Optional:** Define a method called discretize_line() that creates an array on *n* equally spaced points in the line and assigned as a instance attribute.

## Reto 3

1. Create a repo with the class exercise
2. **Restaurant scenario:** You want to design a program to calculate the bill for a customer's order in a restaurant.
- Define a base class *MenuItem*: This class should have attributes like name, price, and a method to calculate the total price.
- Create subclasses for different types of menu items: Inherit from *MenuItem* and define properties specific to each type (e.g., Beverage, Appetizer, MainCourse).
- Define an Order class: This class should have a list of *MenuItem* objects and methods to add items, calculate the total bill amount, and potentially apply specific discounts based on the order composition.

Create a class diagram with all classes and their relationships.
The menu should have at least 10 items.
The code should follow PEP8 rules.


# Diagrams

## Rectangle - Point - Line
```mermaid
classDiagram
    class Point {
        +float x
        +float y
        +move(new_x, new_y)
        +reset()
        +compute_distance(point) float
    }

    class Numerical {
        +float error_diff
        +Point p0
    }

    class Line {
        +Point start
        +Point end
        +float length
        +float slope
        +compute_slope() float
        +compute_length() float
        +compute_horizontal_cross() Point
        +compute_vertical_cross() Point
        +dot(Line) float
        +is_connected(Line) bool
    }

    class Rectangle {
        +float width
        +float height
        +Point center
        +compute_area() float
        +compute_perimeter() float
        +compute_interference_point(Point) bool
    }

    Numerical <|-- Line
    Numerical <|-- Rectangle
    Line *-- Point : composition (2 Points)
    Rectangle *-- Line : composition (4 Lines)
    Rectangle *-- Point : center
```

## Restaurant - Order - MenuItem 
```mermaid
classDiagram
    class MenuItem {
        +string name
        +float price
        +int quantity
        +bool seasonal
    }

    class Dessert {
        +string flavor
        +bool has_alcohol
    }

    class Beverage {
        +string flavor
        +bool has_alcohol
    }

    class MainCourse {
        +string flavor
        +bool has_alcohol
    }

    class Appetizer {
        +string flavor
        +bool has_alcohol
    }

    class Order {
        +list items
        +string client_name
        +float discounts
        +add(MenuItem)
        +remove(MenuItem)
        +define_offers()
        +total() float
        +summary()
    }

    class Restaurant {
        +list orders
        +list items
        +add_order(client_name, items)
    }

    MenuItem <|-- Dessert
    MenuItem <|-- Beverage
    MenuItem <|-- MainCourse
    MenuItem <|-- Appetizer
    Order o-- MenuItem : aggregation
    Restaurant *-- Order : composition
```
