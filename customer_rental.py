#!/usr/bin/python

import random

class Rental:
    def __init__(self, numTools, totalDays, daysRemain, customer): #, tools):
        self.customer = customer
        self.numTools = numTools
        self.totalDays = totalDays
        self.daysRemain = daysRemain
        #self.tools = tools
    def new_day(self):
        self.daysRemain -=1

class Customer:
    def __init__(self, rentals = set()):
        self.rentals = rentals
    def add_rental(self, rental):
        self.rentals.add(rental)
    def initiate_rental(self):
        raise NotImplementedError
    def get_rentals(self):
        return self.rentals

class casualCustomer(Customer):
    def __init__(self, rentals = set()):
        Customer.__init__(self, rentals)
        self.type = "Casual"
    def initiate_rental(self, numTools = random.randint(1,2), numDays = random.randint(1,2)): #add tools
        self.rentals.add(Rental(numTools, numDays, numDays, self)) #add tools


class businessCustomer(Customer):
    def __init__(self, rentals = set()):
        Customer.__init__(self, rentals)
        self.type = "Business"
    def initiate_rental(self): #add tools
        self.rentals.add(Rental(3, 7, 7, self)) #add tools

class regularCustomer(Customer):
    def __init__(self, rentals = set()):
        Customer.__init__(self, rentals)
        self.type = "Regular"
    def initiate_rental(self, numTools = random.randint(1,3), numDays = random.randint(3,5)): #add tools
        self.rentals.add(Rental(numTools, numDays, numDays, self)) #add tools


cust1 = regularCustomer()
cust1.initiate_rental()
