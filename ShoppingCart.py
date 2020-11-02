class Shopping_Cart:

    def __init__(self, order_number):
        self.drinks = {}
        self.pizzas = []
        self.total = 0.0
        self.order_number = order_number
        self.valid_drinks = ["water", "coke", "nestea", "mountain dew", "canada dry"]

    def view_cart(self):
        print("Drinks in cart: ")
        for drinks in self.drinks:
            print(drinks)
            for quantity in self.drinks[drinks]:
                print(quantity, ':', self.drinks[drinks][quantity])

        print("Pizzas in cart:")
        for pizza in self.pizzas:
            print("Pizza Id: ")
            print(pizza.id)
            print("Pizza size: ")
            print(pizza.size)
            print("Pizza dough: ")
            print(pizza.dough)
            print("Pizza toppings: ")
            print(pizza.toppings)
            print("-----------------------------------")

        print("Current subtotal is: " + str(self.total))
        return

    def add_drink(self, drink, quantity):
        print("Drinks: Water, Coke, Nestea, Mountain Dew, Canada Dry")
        if drink.lower() in self.valid_drinks:
            self.drinks[drink.lower()] = self.drinks.get(drink.lower(),0) + quantity
        else:
            print("Invalid drink option, try again.")
        return

    def remove_drink(self, drink, quantity):
        print("Drinks: Water, Coke, Nestea, Mountain Dew, Canada Dry")
        if drink.lower() in self.valid_drinks:
            if self.drinks.get(drink.lower(),0) - quantity >= 0 :
                self.drinks[drink.lower()] = self.drinks.get(drink.lower(),0) - quantity
            else:
                print("You are removing more drinks than you have. Try again.")
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
