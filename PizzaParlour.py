from flask import Flask
from Pizza import *

app = Flask("Assignment 2")

pizza_id = 0


@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'


# PIZZA FUNCTIONS
def choose_pizza(type_flag):
    """
        Chosen pizza will be added to cart object.
    """
    temp_pizza = Pizza(type_flag, pizza_id)
    global pizza_id
    pizza_id += 1
    print("Pizza Sizes: 1 = Small, 2 = Medium, 3 = Large, 4 = Party")
    while(temp_pizza.size == ""):
        tmp_size = input("What size Pizza would you like?")
        temp_pizza.choose_size(tmp_size)
    if(type_flag == 4):
        temp_pizza = create_pizza(temp_pizza)

    return temp_pizza


def create_pizza(custom_pizza):
    # Custom Dough
    print("Pizza Dough: 1 = White, 2 = Whole Wheat, 3 = Cauliflower")
    while(custom_pizza.dough == ""):
        dough_flag = input("What dough would you like?")
        custom_pizza.choose_dough(dough_flag)

    # Custom Toppings
    print("Pizza Toppings: 1 = pepperoni, 2 = bacon, 3 = pineapple, 4 = chicken,\n")
    print("5 = bell peppers, 6 = jalepeno peppers\n Enter 0 to finish topping selection.")
    topping_flag = -1
    while(topping_flag != 0):
        topping_flag = input("What toppings would you like?")
        custom_pizza.add_topping(topping_flag)

    return custom_pizza


def edit_pizza_toppings(pizza):
    # Assuming there is a pizza already in cart, that they want to edit.
    edit_flag = -1
    while(edit_flag != 0):
        print("Edit Pizza: 1 = Change Dough, 2 = Add Toppings, 3 = Remove Toppings, 4 = Change Size\n")
        edit_flag = input("What would you like to change about your pizza?")
        # Change Dough
        if (edit_flag == 1):
            print("Pizza Dough: 1 = White, 2 = Whole Wheat, 3 = Cauliflower")
            pizza.dough = ""
            while(pizza.dough == ""):
                dough_flag = input("What dough would you like?")
                pizza.choose_dough(dough_flag)

        # EDITING TOPPINGS
        # Add Toppings
        if (edit_flag == 2):
            print(
                "Pizza Toppings: 1 = pepperoni, 2 = bacon, 3 = pineapple, 4 = chicken,\n")
            print(
                "5 = bell peppers, 6 = jalepeno peppers\nEnter 0 to finish topping selection.")
            topping_flag = -1
            while(topping_flag != 0):
                topping_flag = input("What toppings would you like to add?")
                pizza.add_topping(topping_flag)

        # Remove Toppings
        if (edit_flag == 3):
            print(pizza.toppings)
            print("Enter the number of the topping you would like to remove.\n Enter 0 to complete topping removal.")
            topping_flag = -1
            while(topping_flag != 0):
                topping_flag = input("What toppings would you like to remove?")
                pizza.remove_topping(topping_flag)
                print(pizza.toppings)

        # Change Size
        if (edit_flag == 4):
            print("Pizza Sizes: 1 = Small, 2 = Medium, 3 = Large, 4 = Party")
            pizza.size = ""
            while(pizza.size == ""):
                size_flag = input("What size pizza would you like?")
                pizza.choose_size(size_flag)


if __name__ == "__main__":
    app.run()
