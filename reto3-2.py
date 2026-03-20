"""
- Restaurant scenario: You want to design a program to 
- calculate the bill for a customer's order in a restaurant.

- Define a base class MenuItem: This class should have attributes
- like name, price, and a method to calculate the total price.
- Create subclasses for different types of menu items: 
- Inherit from MenuItem and define properties specific 
- to each type (e.g., Beverage, Appetizer, MainCourse).

- Define an Order class: This class should have a list 
- of MenuItem objects and methods to add items, calculate 
- the total bill amount, and potentially apply specific 
- discounts based on the order composition.
"""

import random
import copy

class MenuItem:
    def __init__(self, name: str, price: float, seasonal: bool = False):
        self.name = name
        if price < 0:
            price = 0.0
        self.price = price
        self.quantity = 1
        self.seasonal = seasonal

class Dessert(MenuItem):
    def __init__(self, name: str, price: float, seasonal: bool = False):
        super().__init__(name, price, seasonal)
        self.flavor = "sweet"
        self.has_alcohol = False

class MainCourse(MenuItem):
    def __init__(self, name: str, price: float, seasonal: bool = False):
        super().__init__(name, price, seasonal)
        self.flavor = "mixed"
        self.has_alcohol = False

class Appetizer(MenuItem):
    def __init__(self, name: str, price: float, seasonal: bool = False):
        super().__init__(name, price, seasonal)
        self.flavor = "mixed"
        self.has_alcohol = False

class Beverage(MenuItem):
    def __init__(self, name: str, price: float, seasonal: bool = False):
        super().__init__(name, price, seasonal)
        self.flavor = "mixed"
        self.has_alcohol = True

class Order:
    def __init__(self, client_name: str = "default client"):
        self.items = []
        self.client_name = client_name
        self.discounts = 0

    def add(self, item: MenuItem):
        added = False
        for i in self.items:
            if i.name == item.name:
                i.quantity = i.quantity + 1
                added = True
                break
        if not added:
            self.items.append(copy.deepcopy(item))
        

    def remove(self, item: MenuItem):
        for i in self.items:
            if i.name == item.name:
                i.quantity = i.quantity - 1
                if i.quantity == 0:
                    self.items.remove(i)
                break

    def define_offers(self):
        # Logic: If you order a Main Course and a Beverage, get 10% off
        has_main = any(isinstance(i, MainCourse) for i in self.items)
        has_beverage = any(isinstance(i, Beverage) for i in self.items)
    
        if has_main and has_beverage:
            self.discounts = 10

    def total(self):
        s = 0
        self.define_offers()
        for i in self.items:
            s = s + i.price*i.quantity

        return s*(1-self.discounts/100)
    
    def summary(self):
        print(f"Order summary for client: {self.client_name}")
        for i in self.items:
            print(f"{i.name}(x{i.quantity}).............${i.price}")

        print(f"Total.............${self.total()}")


class Restaurant:
    def __init__(self):
        self.orders = []
        self.items_available = []
        self.items = [
            Dessert("Apple Pie", 9.99),
            Dessert("Cherry pie", 8.79),
            Beverage("Wine", 9.89),
            Beverage("Apple juice", 4.44),
            Beverage("Coca Cola", 19.44),
            MainCourse("Hamburguer", 9.99),
            MainCourse("XXL Pizza", 49.99),
            MainCourse("Steak", 29.45),
            MainCourse("Fried Fish", 34.88),
            Appetizer("Mozz Tots", 7.77),
            Appetizer("Baked Caprese Bites", 4.55),
            Appetizer("Crab Rangoon Cups", 6.77),
            Appetizer("Christmas Tree Deviled Eggs", 9.99, True)
        ]

        #! i just generate some items in order to manage "stock"
        for i in range(22):
            self.items_available.append(copy.deepcopy(random.choice(self.items)))

    def add_order(self, client_name: str, *args):
        order = Order(client_name)
        for count, item in enumerate(args):
            order.add(item)

        self.orders.append(order)
    
