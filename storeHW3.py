class Store:
    money = 0  # Total money made so far
    currentRentals = []  # Rentals that have not finished yet
    completedRentals = []  # Rentals that have already completed
    tools = []  # List of all tools (Availability is indicated by the 'available' bool in the Tool class)

    def report(self):  # Creates the final report after day 35, should be called in the Simulation class
        print("There are ", sum(tool.available for tool in self.tools), "tools in the store\nCURRENT TOOLS IN THE "
                                                                        "STORE:\n")
        for tool in self.tools:  # Print all the tools that are available currently
            if tool.available:
                print(tool.name, ", ")  # Will leave a trailing ', ' after the list; fix later
        print("\n\nThe store made ", self.money, " dollars total.\n\nCURRENT RENTALS:\n")
        for rental in self.currentRentals:  # Assumes Rental class has a printRental method
            rental.printRental()
        print("\nACTIVE RENTALS:\n")
        for rental in self.completedRentals:
            rental.printRental()
        return

    def newday(self):  # Does housework in the store for a new day, should be called when appropriate by Simulation
        for rental in self.currentRentals:
            rental.daysLeft -= 1  # Lower remaining days for each current rental by 1
            if rental.daysLeft == 0:  # If the rental is done
                for tool in self.tools:
                    if tool in rental.tools:  # If the specified tool from the store was rented in this rental
                        tool.available = True  # 'Return' it (make it available again)
                self.completedRentals.append(rental)  # Add this rental to the completed rentals list
                self.currentRentals.remove(rental)  # Remove this rental from the current rentals list
        return

    def rent(self, rental):  # Take the incoming rental and process it
        for tool in rental.tools:
            self.money += tool.cost  # Add the cost of the tool to the current money total
            for matchtool in self.tools:
                if matchtool == tool:  # Find the tool requested in the store inventory
                    matchtool.available = False  # 'Rent it out' (make it not available)
        self.currentRentals.append(rental)  # Add this rental to the current rentals list
        return

    def firstday(self):  # TODO: This class will instantiate and name all the tools for the store
        return

    def __init__(self):  # This constructor calls the method which handles everything needed to set up the store
        self.firstday()
        return
