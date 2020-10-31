from flask import Flask
from Pizza.py import Pizza

app = Flask("Assignment 2")


@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'


# PIZZA FUNCTIONS
def choose_pizza(type_flag):
    """
        Chosen pizza will be added to cart object.
    """
    temp_pizza = Pizza(type_flag)
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
    print("5 = bell peppers, 6 = jalepeno peppers")
    topping_flag = -1
    while(topping_flag != 0):
        topping_flag = input("What toppings would you like?")
        custom_pizza.add_topping(topping_flag)

    return custom_pizza


if __name__ == "__main__":
    app.run()
