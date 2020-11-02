from flask import Flask
from Pizza import *
from ShoppingCart import *

app = Flask("Assignment 2")

pizza_id = 0
cart_id = 0
curr_cart = ShoppingCart(cart_id)


@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'


# CART FUNCTIONS
def add_pizza_to_cart(pizza):
    curr_cart.add_pizza(pizza)
    return


def remove_pizza_from_cart(pizza_id):
    curr_cart.remove_pizza(pizza_id)
    return


def add_drink_to_cart(drink, quantity):
    curr_cart.add_drink(drink, quantity)
    return


def remove_drink_from_cart(drink, quantity):
    curr_cart.remove_drink(drink, quantity)
    return


def clear_cart():
    curr_cart.clear_cart()
    return


def view_cart():
    curr_cart.view_cart()
    return


# PIZZA FUNCTIONS
def choose_pizza(type_flag):
    """
        Chosen pizza will be added to cart object.
    """
    global pizza_id
    temp_pizza = Pizza(type_flag, pizza_id)
    pizza_id += 1
    print("Pizza Sizes: 1 = Small, 2 = Medium, 3 = Large, 4 = Party")
    while temp_pizza.size == "":
        tmp_size = input("What size Pizza would you like?")
        temp_pizza.choose_size(tmp_size)
    if type_flag == 4:
        temp_pizza = create_pizza(temp_pizza)

    add_pizza_to_cart(temp_pizza)
    return


def create_pizza(custom_pizza):
    # Custom Dough
    print("Pizza Dough: 1 = White, 2 = Whole Wheat, 3 = Cauliflower")
    while custom_pizza.dough == "":
        dough_flag = input("What dough would you like?")
        custom_pizza.choose_dough(dough_flag)

    # Custom Toppings
    print("Pizza Toppings: 1 = pepperoni, 2 = bacon, 3 = pineapple, 4 = chicken,\n")
    print("5 = bell peppers, 6 = jalepeno peppers\n Enter 0 to finish topping selection.")
    topping_flag = -1
    while topping_flag != 0:
        topping_flag = input("What toppings would you like?")
        custom_pizza.add_topping(topping_flag)

    return custom_pizza


def edit_pizza_toppings(pizza):
    # Assuming there is a pizza already in cart, that they want to edit.
    edit_flag = -1
    while edit_flag != 0:
        print("Edit Pizza: 1 = Change Dough, 2 = Add Toppings, 3 = Remove Toppings, 4 = Change Size\n")
        edit_flag = input("What would you like to change about your pizza?")
        # Change Dough
        if edit_flag == 1:
            print("Pizza Dough: 1 = White, 2 = Whole Wheat, 3 = Cauliflower")
            pizza.dough = ""
            while pizza.dough == "":
                dough_flag = input("What dough would you like?")
                pizza.choose_dough(dough_flag)

        # EDITING TOPPINGS
        # Add Toppings
        if edit_flag == 2:
            print(
                "Pizza Toppings: 1 = pepperoni, 2 = bacon, 3 = pineapple, 4 = chicken,\n")
            print(
                "5 = bell peppers, 6 = jalepeno peppers\nEnter 0 to finish topping selection.")
            topping_flag = -1
            while topping_flag != 0:
                topping_flag = input("What toppings would you like to add?")
                pizza.add_topping(topping_flag)

        # Remove Toppings
        if edit_flag == 3:
            print(pizza.toppings)
            print("Enter the number of the topping you would like to remove.\n Enter 0 to complete topping removal.")
            topping_flag = -1
            while topping_flag != 0:
                topping_flag = input("What toppings would you like to remove?")
                pizza.remove_topping(topping_flag)
                print(pizza.toppings)

        # Change Size
        if edit_flag == 4:
            print("Pizza Sizes: 1 = Small, 2 = Medium, 3 = Large, 4 = Party")
            pizza.size = ""
            while pizza.size == "":
                size_flag = input("What size pizza would you like?")
                pizza.choose_size(size_flag)
    return


def checkout():
    curr_cart.view_cart()
    print("Your total is: " + (curr_cart.total * 1.13))
    global cart_id
    cart_id += 1
    response = input("Do you want to checkout now? y/n")
    while response != "y" or response != "n":
        response = input("Do you want to checkout now? y/n")
    if response == "y":
        #We want to have them choose delivery method here
        return
    elif response == "n":
        return

if __name__ == "__main__":
    app.run()
