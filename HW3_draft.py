import random


class Store:
    money = 0  # Total money made so far
    currentRentals = []  # Rentals that have not finished yet
    completedRentals = []  # Rentals that have already completed
    tools = []  # List of all tools (Availability is indicated by the 'available' bool in the Tool class)

    def report(self):  # Creates the final report after day 35, should be called in the Simulation class
        print("There are ", sum(t.available for t in self.tools), "tools in the store\nCURRENT TOOLS IN THE "
                                                                  "STORE:\n")
        for t in self.tools:  # Print all the tools that are available currently
            if t.check_available():
                print(t.get_name(), ", ")  # Will leave a trailing ', ' after the list; fix later
        print("\n\nThe store made ", self.money, " dollars total.\n\nCURRENT RENTALS:\n")
        for r in self.currentRentals:  # Assumes Rental class has a printRental method
            r.printRental()
        print("\nACTIVE RENTALS:\n")
        for r in self.completedRentals:
            r.printRental()
        return

    def new_day(self):  # Does housework in the store for a new day, should be called when appropriate by Simulation
        for r in self.currentRentals:
            r.new_day()  # Lower remaining days for each current rental by 1
            if r.daysRemain == 0:  # If the rental is done
                for t in self.tools:
                    if t in rental.tools:  # If the specified tool from the store was rented in this rental
                        t.change_available(True)  # 'Return' it (make it available again)
                self.completedRentals.append(rental)  # Add this rental to the completed rentals list
                self.currentRentals.remove(rental)  # Remove this rental from the current rentals list
        return

    def rent(self, in_rental):  # Take the incoming rental and process it
        for t in in_rental.tools:
            self.money += t.get_price()  # Add the cost of the tool to the current money total
            for match_tool in self.tools:
                if match_tool == t:  # Find the tool requested in the store inventory
                    match_tool.change_available(False)  # 'Rent it out' (make it not available)
        self.currentRentals.append(in_rental)  # Add this rental to the current rentals list
        return

    def first_day(self):
        for x in range(1, 5):
            self.tools.append(PaintingTool(x + 1, 1))
        for x in range(5, 9):
            self.tools.append(ConcreteTool(x % 4 + 1, 1))
        for x in range(9, 13):
            self.tools.append(PlumbingTool(x % 4 + 1, 1))
        for x in range(13, 17):
            self.tools.append(YardworkTool(x % 4 + 1, 1))
        for x in range(17, 21):
            self.tools.append(WoodworkTool(x % 4 + 1, 1))
        return

    def get_tools(self):
        return self.tools

    def check_tools(self, num_tools):
        tools = self.get_tools()
        return sum(t.available for t in tools) >= num_tools

    def choose_tools(self, num_tools):
        avail_tools = []
        for t in self.tools:
            if t.available:
                avail_tools.append(t)
        random.shuffle(avail_tools)
        final_tools = avail_tools[0:num_tools]
        return final_tools

    def __init__(self):  # This constructor calls the method which handles everything needed to set up the store
        self.first_day()
        return


class Rental:
    def __init__(self, num_tools, total_days, days_remain, customer, tools):
        self.customer = customer
        self.numTools = num_tools
        self.totalDays = total_days
        self.daysRemain = days_remain
        self.tools = tools

    def new_day(self):
        self.daysRemain -= 1

    def get_rented(self):
        return self.tools


class Customer:
    type = None
    minTools = 0
    maxTools = 0
    minDays = 0
    maxDays = 0

    def __init__(self):
        self.rentals = []

    def add_rental(self, new_rental):
        self.rentals.append(new_rental)

    def initiate_rental(self, shop):
        num_tools = random.randint(self.minTools, self.maxTools)
        num_days = random.randint(self.minDays, self.maxDays)
        if shop.check_tools(num_tools):
            self.rentals.append(Rental(num_tools, num_days, num_days, self, shop.choose_tools(num_tools)))  # add tool

    def get_rentals(self):
        return self.rentals


class CasualCustomer(Customer):
    type = "Casual"
    minTools = 1
    maxTools = 2
    minDays = 1
    maxDays = 2


class BusinessCustomer(Customer):
    type = "Business"
    minTools = 3
    maxTools = 3
    minDays = 7
    maxDays = 7


class RegularCustomer(Customer):
    type = "Regular"
    minTools = 1
    maxTools = 3
    minDays = 3
    maxDays = 5


class Tool:
    base_price = None
    tool_type = None

    def __init__(self, name, available):
        self.name = self.tool_type + " Tool %d" % name
        self.available = available
        change = random.randint(-2, 2)
        self.tool_price = self.base_price + change

    def check_available(self):
        return self.available

    def change_available(self, new_avail):
        self.available = new_avail
        return

    def get_name(self):
        return self.name

    def get_price(self):
        return self.tool_price


class PaintingTool(Tool):
    tool_type = "Painting"
    base_price = 7


class ConcreteTool(Tool):
    tool_type = "Concrete"
    base_price = 18


class PlumbingTool(Tool):
    tool_type = "Plumbing"
    base_price = 15


class WoodworkTool(Tool):
    tool_type = "Woodwork"
    base_price = 10


class YardworkTool(Tool):
    tool_type = "Yardwork"
    base_price = 12


store = Store()
store.first_day()
bob = BusinessCustomer()
bob.initiate_rental(store)
for rental in bob.get_rentals():
    for tool in rental.get_rented():
        print(tool.get_name())
