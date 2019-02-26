import random
import numpy as np

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
                print(t.get_name(), ", ", end="")  # Will leave a trailing ', ' after the list; fix later
        print("\n\nThe store made ", self.money, " dollars total.\n\nCURRENT RENTALS:\n")
        for r in self.currentRentals:  # Assumes Rental class has a printRental method
            r.print_rental()
        print("\nCOMPLETED RENTALS::\n")
        for r in self.completedRentals:
            r.print_rental()
        return

    def new_day(self):  # Does housework in the store for a new day, should be called when appropriate by Simulation
        for r in self.currentRentals:
            r.new_day()  # Lower remaining days for each current rental by 1
            if r.get_days_left() == 0:  # If the rental is done
                for t in self.tools:
                    if t in r.get_rented():  # If the specified tool from the store was rented in this rental
                        t.change_available(True)  # 'Return' it (make it available again)
                self.completedRentals.append(r)  # Add this rental to the completed rentals list
                self.currentRentals.remove(r)  # Remove this rental from the current rentals list
        return

    def rent(self, in_rental):  # Take the incoming rental and process it
        self.money += in_rental.get_price()  # Add the cost of the tool to the current money total
        for t in in_rental.get_rented():
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
        self.total_days = total_days
        self.daysRemain = days_remain
        self.tools = tools
        self.price = self.get_price()

    def new_day(self):
        self.daysRemain -= 1

    def get_days_left(self):
        return self.daysRemain

    def get_rented(self):
        return self.tools

    def get_price(self):
        total = 0
        for t in self.tools:
            total += t.get_price()
        return total

    def print_rental(self):
        print("RENTAL INFO:")
        print("Customer: " + self.customer.get_name())
        print("Tools: ", end="")
        for t in self.tools:
            print(t.get_name(), ", ", end="")
        print("")
        print("Days:", self.total_days)
        print("Total cost:", self.price)


class Customer:
    type = None
    minTools = 0
    maxTools = 0
    minDays = 0
    maxDays = 0

    def __init__(self, name):
        self.rentals = []
        self.name = self.type + " Customer %d" % name

    def add_rental(self, new_rental):
        self.rentals.append(new_rental)

    def initiate_rental(self, shop):
        num_tools = random.randint(self.minTools, self.maxTools)
        num_days = random.randint(self.minDays, self.maxDays)
        if shop.check_tools(num_tools):
            to_rent = Rental(num_tools, num_days, num_days, self, shop.choose_tools(num_tools))
            self.rentals.append(to_rent)  # add tool
            shop.rent(to_rent)

    def get_rentals(self):
        return self.rentals

    def get_name(self):
        return self.name


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

class Simulation():
    day = 1
    customers = []

    def create_customers(self):
        cas_count = 1
        bus_count = 1
        reg_count = 1
        for i in range(1, 11):
            choice = random.randint(1, 3)
            if choice == 1:
                # casual
                self.customers.append(CasualCustomer(cas_count))
                cas_count += 1
                pass

            elif choice == 2:
                # business
                self.customers.append(BusinessCustomer(bus_count))
                bus_count += 1

            elif choice == 3:
                # regular
                self.customers.append(RegularCustomer(reg_count))
                reg_count += 1

    def run_sim(self):
        store = Store()
        store.first_day()
        while self.day <= 35:

            store.new_day()
            #generate number of customers for the day
            num_customers = random.randint(1,10)
            customer_inds = np.random.choice(10, num_customers, replace=False)
            for ind in customer_inds:
                self.customers[ind].initiate_rental(store)
            self.day += 1
        store.report()





    def __init__(self):
        self.create_customers()


if __name__ == '__main__':
    sim = Simulation()
    sim.run_sim()


