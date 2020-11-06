from flask import Flask
from flask import request
from Pizza import *
from ShoppingCart import *
import json

app = Flask("Assignment 2")

pizza_id = 0
cart_id = 0
curr_cart = ShoppingCart(cart_id)


@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'


# CART FUNCTIONS
@app.route('/cart')
def get_cart():
    return curr_cart


@app.route('/cart-string')
def get_cart_string():
    return curr_cart.view_cart()


@app.route('/drinks-in-cart')
def get_drinks_in_cart():
    return curr_cart.get_drinks()


@app.route('/valid-drinks')
def get_valid_drinks():
    return curr_cart.view_valid_drinks()


def add_pizza_to_cart(pizza):
    curr_cart.add_pizza(pizza)
    return


def remove_pizza_from_cart(pizza_id):
    curr_cart.remove_pizza(pizza_id)
    return


@app.route('/add-drink/<drink>/<quantity>', methods=['GET', 'POST'])
def add_drink_to_cart(drink, quantity):
    curr_cart.add_drink(drink, int(quantity))
    if drink.lower() in curr_cart.view_valid_drinks():
        return "Drink added"
    else:
        return "Invalid drink. Try again."


@app.route('/remove-drink/<drink>/<quantity>', methods=['GET', 'POST'])
def remove_drink_from_cart(drink, quantity):
    curr_cart.remove_drink(drink, int(quantity))
    if curr_cart.drinks.get(drink.lower()):
        return_string = "Drink removed"
    else:
        return_string = "Invalid drink. Try again."
    return return_string


@app.route('/clear-cart')
def clear_cart():
    curr_cart.clear_cart()
    return "Cart Cleared"


@app.route('/is-pizza-in-cart/<id>', methods=['GET', 'POST'])
def is_pizza_in_cart(id):
    for pizza in curr_cart.pizzas:
        if pizza.id == id:
            return True
    return False

# Menu Functions


@app.route('/view-menu')
def view_menu():
    menu = open("Menu.txt", "r")
    return menu.readlines


@app.route('/parse-menu/<order_item>', methods=['GET', 'POST'])
def parse_menu(order_item):
    toppings = ["pepperoni", "bacon", "pineapple", "pineapples", "chicken",
                "bell peppers", "jalapeno peppers", "bell pepper", "jalapeno pepper"]
    dough = ["white", "whole wheat", "cauliflower"]
    return_string = ""
    # Pizza Options
    if order_item.lower() == "pepperoni pizza":
        return_string = "One of the Kanuli specials. Made on White Bread Dough \n \
            (S: 9/ M: 11/ L: 13/ P: 18)"
    elif order_item.lower() == "cheese pizza":
        return_string = "One of the Kanuli specials. Made on White Bread Dough \n \
            (S: 9/ M: 11/ L: 13/ P: 18)"
    elif order_item.lower() == "meat lover's pizza" or "meat lovers pizza":
        return_string = "One of the Kanuli specials. Made on White Bread Dough \n \
            (S: 11/ M: 13/ L: 15/ P: 20)"
    elif order_item.lower() == "pizza":
        return_string = "Yup, that's what we serve. You can make your own or get a special.\n \
                Prices may vary based on size, dough, and number of toppings."
    # Dough
    elif order_item.lower() in dough:
        return_string = "This item is a possible dough base for a pizza.\
            (White: 3/ WW: 3.50/ Cauliflower: 4)"
    # Topping Options
    elif order_item.lower() == "cheese":
        return_string = "Cheese is automatically applied to all pizzas. It's on the house."
    elif order_item.lower() in toppings:
        return_string = "This item is a possible topping for a pizza.\
            One topping is on the house, additional toppings are $1 each."
    else:
        return_string = "This item isn't recognized. Perhaps view full menu to check?"
    return return_string


# PIZZA FUNCTIONS
@app.route('/choose-pizza/<type_flag>/<size_option>', methods=['GET', 'POST'])
def choose_pizza(type_flag, size_option):
    global pizza_id
    temp_pizza = Pizza(int(type_flag), pizza_id)
    pizza_id += 1
    temp_pizza.choose_size(int(size_option))
    add_pizza_to_cart(temp_pizza)
    return "Pizza added to cart."


@app.route('/create-pizza/<dough_option>/<toppings_option>/<size_option>', methods=['GET', 'POST'])
def create_pizza(dough_option, toppings_option, size_option):
    global pizza_id
    custom_pizza = Pizza(4, pizza_id)
    pizza_id += 1
    custom_pizza.choose_dough(dough_option)

    for x in toppings_option.split(","):
        custom_pizza.add_topping(int(x))

    custom_pizza.choose_size(size_option)
    add_pizza_to_cart(custom_pizza)
    return "Pizza added to cart."


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
        # We want to have them choose delivery method here
        return
    elif response == "n":
        return

def ubereats_json_generation(address, order_details):
    order = {"Order address": address,
         "Order details": order_details,
         "Order number": cart_id}
    json_string = json.dumps(order)
    return json_string


if __name__ == "__main__":
    app.run()
