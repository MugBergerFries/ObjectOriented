import random


class Tool:
    def __init__(self, name, available):
        self.name = name
        self.available = available
        
    def check_available(self):
        if self.available == True:
            return True
        else:
            return False
            
    def generate_price(self, base_price):
        change = random.randint(-2,2)
        tool_price = base_price + change 
        return tool_price
        
        
class painting_tool(Tool):
    def __init__(self, name, available):
        Tool.__init__(self, name, available)
        self.name = name
        self.available = available
        self.base_cost = 7
        self.tool_cost = Tool.generate_price(self, self.base_cost)
        
class concrete_tool(Tool):
    def __init__(self, name,available):
        Tool.__init__(self, name, available)
        self.name = name
        self.available = available
        self.base_cost = 18
        self.tool_cost = Tool.generate_price(self, self.base_cost)


class plumbing_tool(Tool):
    def __init__(self, name, available):
        Tool.__init__(self, name, available)
        self.name = name
        self.available = available
        self.base_cost = 15
        self.tool_cost = Tool.generate_price(self, self.base_cost)
        
        
class woodwork_tool(Tool):
    def __init__(self, name,available):
        Tool.__init__(self, name, available)
        self.name = name
        self.available = available
        self.base_cost = 10
        self.tool_cost = Tool.generate_price(self, self.base_cost)
        
        
class yardwork_tool(Tool):
    def __init__(self, name, available):
        Tool.__init__(self, name, available)
        self.name = name
        self.available = available
        self.base_cost = 12
        self.tool_cost = Tool.generate_price(self, self.base_cost)

#Yardwork tools for sim
hoe = yardwork_tool('Hoe', True)
shovel = yardwork_tool('Shovel', True)
rake = yardwork_tool('Rake', True)
chainsaw = yardwork_tool('Chainsaw', True)


#Woodwork tools for sim
saw = woodwork_tool('Saw', True)
hammer = woodwork_tool('Hammer', True)
sander = woodwork_tool('Sander', True)
workbench = woodwork_tool('Workbench', True)


print(hoe.tool_cost)
