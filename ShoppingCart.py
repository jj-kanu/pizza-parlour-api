class ShoppingCart:

    def __init__(self, order_number):
        self.drinks = {}
        self.pizzas = []
        self.total = 0.0
        self.order_number = order_number
        self.valid_drinks = ["water", "coke", "nestea", "mountain dew", "canada dry"]

    def view_valid_drinks(self):
        curr_string = "Drinks: "
        i = 0
        while i < len(self.valid_drinks):
            curr_string += self.valid_drinks[i]
            if i != len(self.valid_drinks) - 1:
                curr_string += ', '
            i += 1
        return curr_string

    def view_cart(self):
        curr_string = "Current Cart:\n"
        curr_string += "------------------------------\n"
        curr_string += "Drinks in cart: \n"
        for drinks in self.drinks:
            curr_string += "* "
            curr_string += drinks
            curr_string += ':'
            curr_string += str(self.drinks[drinks])
            curr_string += "\n"

        curr_string += "\nPizzas in cart:"
        for pizza in self.pizzas:
            topping_array = []
            curr_string += "\nPizza Id: "
            curr_string += str(pizza.id)
            curr_string += "\nPizza size: "
            curr_string += pizza.size
            curr_string += "\nPizza dough: "
            curr_string += pizza.dough
            curr_string += "\nPizza toppings: "
            for topping in pizza.toppings:
                topping_array.append(pizza.toppings[topping])
            curr_string += str(topping_array)
            curr_string += "\n-----------------------------------"

        curr_string += "\nCurrent subtotal is: " + str(self.total)
        return curr_string

    def add_drink(self, drink, quantity):
        if drink.lower() in self.valid_drinks:
            self.drinks[drink.lower()] = self.drinks.get(drink.lower(),0) + quantity
            self.total += (1.5 * quantity)
        else:
            print("Invalid drink option, try again.")
        return

    def remove_drink(self, drink, quantity):
        print("Drinks: Water, Coke, Nestea, Mountain Dew, Canada Dry")
        if drink.lower() in self.valid_drinks:
            if self.drinks.get(drink.lower(),0) - quantity >= 0 :
                self.drinks[drink.lower()] = self.drinks.get(drink.lower(),0) - quantity
                self.total -= (1.5 * quantity)
            else:
                return_string = ("You are removing more drinks than you have. Try again.")
        else:
            print("Invalid drink option, try again.")
        return

    def add_pizza(self, pizza):
        self.pizzas.append(pizza)
        self.total += pizza.price
        return

    def remove_pizza(self, pizzaId):
        for pizza in self.pizzas:
            if pizza.id == pizzaId:
                self.total -= pizza.price
                self.pizzas.remove(pizza)
            else:
                print("Invalid pizza removal.")
        return

    def clear_cart(self):
        self.drinks = {}
        self.pizzas = []
        self.total = 0.0
        print("Cart cleared!")
        return

    def get_drinks(self):
        return self.drinks
