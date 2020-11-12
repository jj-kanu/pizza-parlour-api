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
    return 'Welcome to Kanuli\'s Pizza!'


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




def add_pizza_to_cart(pizza):
    curr_cart.add_pizza(pizza)
    return











# Menu Functions


@app.route('/view-menu')
def view_menu():
    menu = open("Menu.txt", "r")
    temp = menu.readlines()
    returning_menu = ""
    for line in temp:
        returning_menu += line
    return returning_menu


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
    elif order_item.lower() == "meat lover's pizza" or order_item.lower == "meat lovers pizza":
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
        return_string = "This item is a possible topping for a pizza. \n \
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
    temp_pizza.calculate_price()
    add_pizza_to_cart(temp_pizza)
    return "Pizza added to cart."


@app.route('/create-pizza/<dough_option>/<toppings_option>/<size_option>', methods=['GET', 'POST'])
def create_pizza(dough_option, toppings_option, size_option):
    global pizza_id
    custom_pizza = Pizza(4, pizza_id)
    pizza_id += 1
    custom_pizza.choose_dough(int(dough_option))

    for x in toppings_option.split(","):
        custom_pizza.add_topping(int(x))

    custom_pizza.choose_size(int(size_option))
    custom_pizza.calculate_price()
    add_pizza_to_cart(custom_pizza)
    return "Pizza added to cart."

# Edit Pizza Functions


@app.route('/change-pizza-dough/<pizza_id>/<dough_option>', methods=['GET', 'POST'])
def change_pizza_dough(pizza_id, dough_option):
    previous_price = 0.0
    curr_price = 0.0
    for pizza in curr_cart.pizzas:
        if pizza.id == int(pizza_id):
            previous_price = pizza.price
            pizza.choose_dough(int(dough_option))
            pizza.calculate_price()
            curr_price = pizza.price
            curr_cart.update_price(previous_price, curr_price)
    return "Dough has been changed."


@app.route('/change-pizza-size/<pizza_id>/<size_option>', methods=['GET', 'POST'])
def change_pizza_size(pizza_id, size_option):
    previous_price = 0.0
    curr_price = 0.0
    for pizza in curr_cart.pizzas:
        if pizza.id == int(pizza_id):
            previous_price = pizza.price
            pizza.choose_size(int(size_option))
            pizza.calculate_price()
            curr_price = pizza.price
            curr_cart.update_price(previous_price, curr_price)
    return "Size has been changed."


@app.route('/add-topping-to-pizza/<pizza_id>/<toppings_option>', methods=['GET', 'POST'])
def add_topping_to_pizza(pizza_id, toppings_option):
    previous_price = 0.0
    curr_price = 0.0
    for pizza in curr_cart.pizzas:
        if pizza.id == int(pizza_id):
            for x in toppings_option.split(","):
                previous_price = pizza.price
                pizza.add_topping(int(x))
                pizza.calculate_price()
                curr_price = pizza.price
                curr_cart.update_price(previous_price, curr_price)
    return "These toppings will be added to Pizza."


@app.route('/remove-topping-from-pizza/<pizza_id>/<toppings_option>', methods=['GET', 'POST'])
def remove_topping_from_pizza(pizza_id, toppings_option):
    previous_price = 0.0
    curr_price = 0.0
    for pizza in curr_cart.pizzas:
        if pizza.id == int(pizza_id):
            for x in toppings_option.split(","):
                previous_price = pizza.price
                pizza.remove_topping(int(x))
                pizza.calculate_price()
                curr_price = pizza.price
                curr_cart.update_price(previous_price, curr_price)
    return "These toppings will not be on your Pizza."


@app.route('/json-generation/<address>', methods=['GET', 'POST'])
def ubereats_json_generation(address):
    order_details = ""
    if curr_cart.drinks and not curr_cart.pizzas:
        order_details += address + ", No Pizzas , No Pizza Prices, " + str(curr_cart.drinks) + \
            " ($1.50 each), " + str(cart_id) + "\n"
        return order_details
    for pizza in curr_cart.pizzas:
        order_details += pizza.size + ": " + str(pizza.toppings) + ", " + \
            str("${:,.2f}".format(pizza.price)) + ", " + str(curr_cart.drinks) + \
            " ($1.50 each), " + "\n"
    order = {
        "Order number": cart_id,
        "Order address": address,
        "Order details": order_details
    }
    json_string = json.dumps(order, indent=4, sort_keys=True)
    return json_string


@app.route('/csv-generation/<address>', methods=['GET', 'POST'])
def csv_generation(address):
    csv_string = "Order address:, Order Details/Pizza, Order Details/Price,\
        Order Details/Drinks, Order Number\n"
    if curr_cart.drinks and not curr_cart.pizzas:
        csv_string += address + ", No Pizzas , No Pizza Prices, " + str(curr_cart.drinks) + \
            " ($1.50 each), " + str(cart_id) + "\n"
        return csv_string
    for pizza in curr_cart.pizzas:
        csv_string += address + ", " + pizza.size + ": " + str(pizza.toppings) + ", " + \
            str("${:,.2f}".format(pizza.price)) + ", " + str(curr_cart.drinks) + \
            " ($1.50 each), " + str(cart_id) + "\n"
    return csv_string

@app.route('/complete-order')
def complete_order():
    global curr_cart
    global cart_id
    cart_id += 1
    curr_cart = ShoppingCart(cart_id)
    return "Order completed"

if __name__ == "__main__":
    app.run()
