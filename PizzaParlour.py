from flask import Flask
from flask import request
from Pizza import *
from ShoppingCart import *
import json

app = Flask("Assignment 2")

cart_id = 0
curr_cart = ShoppingCart(cart_id)


@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Kanuli\'s Pizza!'


# CART FUNCTIONS
@app.route('/cart')
def get_cart():
    return str(curr_cart.order_number)


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


@app.route('/csv-generation/<csv_string>', methods=['GET', 'POST'])
def csv_generation(csv_string):
    print("Server recieved csv: " + csv_string)
    return "Done"


@app.route('/complete-order')
def complete_order():
    global curr_cart
    global cart_id
    cart_id += 1
    curr_cart = ShoppingCart(cart_id)
    return "Order completed"


if __name__ == "__main__":
    app.run()
