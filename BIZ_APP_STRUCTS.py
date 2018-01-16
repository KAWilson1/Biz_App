#Author: Kyle Wilson
#Init: 1/13/18
#Last updated: 1/13/18
#Purpose: Create data structs for Orders and Items
import datetime
from datetime import date


class Order():
    def __init__(self, orderID, cart, myDate):
        if type(orderID) != int:
            raise Exception("First argument for Order must be an int")
        if type(cart) != list:
            raise Exception("Second argument for Order must be an list")
        if type(myDate) != datetime.date:
            raise Exception("Third argument for Order must be datetime.date")

        self.orderID = orderID
        self.cart = cart
        self.myDate = myDate

    def get_ID(self):
        return self.orderID

    def get_cart(self):
        return self.cart

    def get_date(self):
        return self.myDate

    def add_item(self, item):
        self.cart.append(item)

class Item():
    def __init__(self, itemID, name, cost, taxable):
        self.itemID = itemID
        self.name = name
        self.cost = cost
        self.taxable = taxable

    def get_ID(self):
        return self.itemID

    def get_name(self):
        return self.name

    def get_cost(self):
        return self.cost

    def get_taxable(self):
        return self.taxable


