import random


class Store:
    money = 0  # Total money made so far
    currentRentals = []  # Rentals that have not finished yet
    completedRentals = []  # Rentals that have already completed
    tools = []  # List of all tools (Availability is indicated by the 'available' bool in the Tool class)

    def report(self):  # Creates the final report after day 35, should be called in the Simulation class
        print("There are ", sum(tool.available for tool in self.tools), "tools in the store\nCURRENT TOOLS IN THE "
                                                                        "STORE:\n")
        for tool in self.tools:  # Print all the tools that are available currently
            if tool.check_available():
                print(tool.get_name(), ", ")  # Will leave a trailing ', ' after the list; fix later
        print("\n\nThe store made ", self.money, " dollars total.\n\nCURRENT RENTALS:\n")
        for rental in self.currentRentals:  # Assumes Rental class has a printRental method
            rental.printRental()
        print("\nACTIVE RENTALS:\n")
        for rental in self.completedRentals:
            rental.printRental()
        return

    def new_day(self):  # Does housework in the store for a new day, should be called when appropriate by Simulation
        for rental in self.currentRentals:
            rental.new_day()  # Lower remaining days for each current rental by 1
            if rental.daysRemain == 0:  # If the rental is done
                for tool in self.tools:
                    if tool in rental.tools:  # If the specified tool from the store was rented in this rental
                        tool.change_available(True)  # 'Return' it (make it available again)
                self.completedRentals.append(rental)  # Add this rental to the completed rentals list
                self.currentRentals.remove(rental)  # Remove this rental from the current rentals list
        return

    def rent(self, rental):  # Take the incoming rental and process it
        for tool in rental.tools:
            self.money += tool.get_price()  # Add the cost of the tool to the current money total
            for match_tool in self.tools:
                if match_tool == tool:  # Find the tool requested in the store inventory
                    match_tool.change_available(False)  # 'Rent it out' (make it not available)
        self.currentRentals.append(rental)  # Add this rental to the current rentals list
        return

    def first_day(self):
        for x in range(1, 5):
            self.tools.append(PaintingTool(x, 1))
        for x in range(5, 9):
            self.tools.append(ConcreteTool(x, 1))
        for x in range(9, 13):
            self.tools.append(PlumbingTool(x, 1))
        for x in range(13, 17):
            self.tools.append(YardworkTool(x, 1))
        for x in range(17, 21):
            self.tools.append(WoodworkTool(x, 1))
        return

    def __init__(self):  # This constructor calls the method which handles everything needed to set up the store
        self.first_day()
        return


class Rental:
    def __init__(self, num_tools, total_days, days_remain, customer):  # , tools):
        self.customer = customer
        self.numTools = num_tools
        self.totalDays = total_days
        self.daysRemain = days_remain
        # self.tools = tools

    def new_day(self):
        self.daysRemain -= 1


class Customer:
    type = None
    minTools = None
    maxTools = None
    minDays = None
    maxDays = None


    def __init__(self):
        self.rentals = []

    def add_rental(self, rental):
        self.rentals.append(rental)

    def initiate_rental(self, num_tools=random.randint(minTools, maxTools),
                        num_days=random.randint(minDays, maxDays)):  # add tools
        self.rentals.append(Rental(num_tools, num_days, num_days, self))  # add tools

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

    def chck_available(self):
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
