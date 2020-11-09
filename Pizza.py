class Pizza:
    def __init__(self, type, id):
        self.id = id
        self.toppings = {}
        self.size = ""
        self.price = 0.0
        self.dough = ""
        if(type == 1):
            self.dough = "White"
            self.toppings = {1: "pepperoni"}
            self.size = ""
            self.price = 0.0
        elif(type == 2):
            # Cheese Pizza
            self.dough = "White"
            self.toppings = {}
            self.size = ""
            self.price = 0.0
        elif(type == 3):
            # Meat Lovers
            self.dough = "White"
            self.toppings = {1: "pepperoni", 2: "bacon", 4: "chicken"}
            self.size = ""
            self.price = 0.0
        elif(type == 4):
            self.dough = ""
            self.toppings = {}
            self.size = ""
            self.price = 0.0

    def add_topping(self, topping_flag):
        if(topping_flag == 1):
            self.toppings[1] = "pepperoni"
        elif(topping_flag == 2):
            self.toppings[2] = "bacon"
        elif(topping_flag == 3):
            self.toppings[3] = "pineapples"
        elif(topping_flag == 4):
            self.toppings[4] = "chicken"
        elif(topping_flag == 5):
            self.toppings[5] = "bell peppers"
        elif(topping_flag == 6):
            self.toppings[6] = "jalepeno peppers"

    def remove_topping(self, topping_flag):
        if(topping_flag in self.toppings):
            self.toppings.pop(topping_flag)

    def choose_dough(self, dough_flag):
        if(dough_flag == 1):
            self.dough = "White"
        elif(dough_flag == 2):
            self.dough = "Whole Wheat"
        elif(dough_flag == 3):
            self.dough = "Cauliflower"

    def choose_size(self, size_flag):
        if(size_flag == 1):
            self.size = "Small"
        elif(size_flag == 2):
            self.size = "Medium"
        elif(size_flag == 3):
            self.size = "Large"
        elif(size_flag == 4):
            self.size = "Party Size"

    def calculate_price(self):
        # Dough Prices
        self.price = 0
        if(self.dough == "White"):
            self.price += 3
        elif(self.dough == "Whole Wheat"):
            self.price += 3.50
        elif(self.dough == "Cauliflower"):
            self.price += 4

        # Size Prices
        if(self.size == "Small"):
            self.price += 6
        elif(self.size == "Medium"):
            self.price += 8
        elif(self.size == "Large"):
            self.price += 10
        elif(self.size == "Party Size"):
            self.price += 15

        # Toppings Prices
        if(len(self.toppings) > 0):
            self.price += (len(self.toppings) - 1) * 1

        return
