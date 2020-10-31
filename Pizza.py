class Pizza:
    def __init__(self, dough, size):
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
        else:
            print("Please enter a valid topping option.")

    def remove_topping(self, topping_flag):
        if(self.toppings[topping_flag]):
            self.toppings.pop(topping_flag)

    def choose_dough(self, dough_flag):
        if(dough_flag == 1):
            self.dough = "White"
        elif(dough_flag == 2):
            self.dough = "Whole Wheat"
        elif(dough_flag == 3):
            self.dough = "Cauliflower"
        else:
            print("Please enter a valid dough option.")

    def choose_size(self, size_flag):
        if(size_flag == 1):
            self.size = "Small"
        elif(size_flag == 2):
            self.size = "Medium"
        elif(size_flag == 3):
            self.size = "Large"
        elif(size_flag == 4):
            self.size = "Party Size"
        else:
            print("Please enter a valid size option.")
