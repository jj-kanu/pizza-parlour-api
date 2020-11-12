import sys
import requests
from Pizza import *
from ShoppingCart import *

pizza_id = 0

#Initialize the cart
curr_cart = None


def get_cart_id():
    response = requests.get("http://127.0.0.1:5000/cart")
    cart_id = int(response.text)
    return cart_id

def set_cart(cart_id):
    global curr_cart
    curr_cart = ShoppingCart(cart_id)

def get_client_cart():
    return curr_cart

def main():
    response = requests.get("http://127.0.0.1:5000/pizza")
    print(response.text)
    set_cart(get_cart_id())
    main_menu_input = main_menu_prompt()
    while accept_input(main_menu_input) != '0':
        main_menu_input = main_menu_prompt()
    return


def add_pizza_to_cart(pizza):
    curr_cart.add_pizza(pizza)
    return


def main_menu_prompt():
    print("\n===============================================================================")
    print("Menu Commands:")
    print("-------------------------------------------------------------------------------")
    print("1: Add Pizza to Cart, 2: Remove Pizza from Cart, 3: Edit Pizza in Cart")
    print("4: Add Drink to Cart, 5: Remove Drink from Cart")
    print("6: View Cart, 7: Cancel Order, 8: View Menu, 9: Look up Menu Item")
    print("Administrative Access - Edit Price of Pizza in Cart: Enter 98")
    print("Administrative Access - Edit Price of Drinks in Cart: Enter 99")
    return input("Enter 10 to checkout or 0 to exit: ")


def accept_input(main_menu_input):
    if main_menu_input == "1":
        print(
            "Enter 1 for Pepperoni, 2 for Cheese, 3 for Meat Lover's, 4 for Custom Pizza.")
        pizza_option = input("What type of pizza would you like? ")
        while int(pizza_option) not in range(1, 5):
            print("Invalid pizza type. Please enter a valid pizza type.")
            pizza_option = input("What type of pizza would you like? ")
        # PREMADE PIZZAS
        if int(pizza_option) in range(1, 4):
            premade_size_choice(pizza_option)
        # CUSTOM PIZZAS
        elif int(pizza_option) == 4:
            # Dough
            dough_option = custom_choose_dough()
            # Toppings
            list_of_toppings = custom_choose_topping()
            # Size
            size_option = choose_pizza_size()

            custom_pizza_creation(dough_option, list_of_toppings, size_option)

    # Remove Pizza
    if main_menu_input == "2":
        remove_pizza()

    # Edit Pizza
    if main_menu_input == "3":
        client_view_cart()

        pizza_id = input("What is the id of the pizza you want to edit? ")
        pizza_exists = is_pizza_in_cart(pizza_id)
        # Checks if Pizza is in cart
        if pizza_exists == "":
            edit_flag = -1
            while int(edit_flag) != 0:
                print(
                    "Edit Pizza: 1 = Change Dough, 2 = Add Toppings, 3 = Remove Toppings, 4 = Change Size\n\
                        Enter 0 to confirm changes and return to menu.")
                edit_flag = input(
                    "What would you like to change about your pizza? ")
                # Edit Dough
                if int(edit_flag) == 1:
                    edit_dough(pizza_id)
                # Add Toppings
                elif int(edit_flag) == 2:
                    edit_toppings(pizza_id)

                # Remove Toppings
                elif int(edit_flag) == 3:
                    remove_toppings(pizza_id)

                # Edit size
                elif int(edit_flag) == 4:
                    edit_size(pizza_id)
                else:
                    print(
                        "Please pick a valid edit option or enter 0 to go back to menu.")
        else:
            print(pizza_exists)

    # Extract this out to helper functions
    if main_menu_input == "4":
        client_add_drinks()

    if main_menu_input == "5":
        are_there_drinks_in_cart()
        client_remove_drinks()

    if main_menu_input == "6":
        client_view_cart()

    if main_menu_input == "7":
        client_clear_cart()

    if main_menu_input == "8":
        view_menu()

    if main_menu_input == "9":
        parse_menu()

    if main_menu_input == "10":
        checkout()

    if main_menu_input == "98":
        client_view_cart()

        pizza_id = input(
            "What is the id of the pizza you want to change price? ")
        pizza_exists = pizza_exists(pizza_id)
        # Checks if Pizza is in cart
        if pizza_exists == "":
            new_price = input("What is this pizza's new price? $")
            while not is_price_float(new_price):
                new_price = input(
                    "What is this pizza's new price?(Enter in dollars) $")
            if float(new_price) < 0:
                print("This is an invalid price. Price will not be changed")
                return
            for pizza in curr_cart.pizzas:
                if pizza.id == int(pizza_id):
                    previous_price = pizza.price
                    pizza.price = float(new_price)
                    curr_cart.update_price(previous_price, pizza.price)
            print("Price of Pizza " + pizza_id + " has been changed to $" + new_price)
        else:
            print(pizza_exists)

    if main_menu_input == "99":
        client_view_cart()
        drinks_in_cart = are_there_drinks_in_cart()
        if drinks_in_cart == "":
            return
        else:
            print(drinks_in_cart)
    return main_menu_input


def premade_size_choice(pizza_option):
    size_option = choose_pizza_size()
    global pizza_id
    temp_pizza = Pizza(int(pizza_option), pizza_id)
    pizza_id += 1
    temp_pizza.choose_size(int(size_option))
    temp_pizza.calculate_price()
    add_pizza_to_cart(temp_pizza)
    print("Pizza added to cart.")


def custom_pizza_creation(dough, topping, size):
    global pizza_id
    custom_pizza = Pizza(4, pizza_id)
    pizza_id += 1
    custom_pizza.choose_dough(int(dough))

    for x in topping.split(","):
        custom_pizza.add_topping(int(x))

    custom_pizza.choose_size(int(size))
    custom_pizza.calculate_price()
    add_pizza_to_cart(custom_pizza)
    print("Pizza added to cart.")


def choose_pizza_size():
    print("Enter 1 for Small, 2 for Medium, 3 for Large, 4 for Party Size.")
    size_option = input("What size pizza do you want? ")
    while int(size_option) not in range(1, 5):
        print("Invalid size. Please enter a valid pizza size flag.")
        size_option = input("What size pizza do you want? ")
    return size_option


def custom_choose_topping():
    print("Enter Topping Number: 1: pepperoni, 2:bacon, 3:pineapple, 4:chicken,\n \
                5: bell peppers, 6: jalapeno peppers")
    print("Enter 0 to Stop Adding Toppings")
    list_of_toppings = ""
    topping_option = -1
    while int(topping_option) != 0:
        topping_option = input("What toppings do you want to add? ")
        if int(topping_option) in range(1, 7):
            list_of_toppings += str(topping_option) + ","
            print("Topping added.")
        elif int(topping_option) == 0:
            list_of_toppings = list_of_toppings[:-1]
            print("Nice choice!")
        else:
            print("Please enter a topping number or press 0 to stop.")
    return list_of_toppings


def custom_choose_dough():
    print("Enter 1 for White, 2 for Whole Wheat, 3 for Cauliflower")
    dough_option = input("What type of dough would you like? ")
    while int(dough_option) not in range(1, 4):
        print("Invalid dough type. Please enter a valid dough type flag.")
        dough_option = input("What type of dough would you like? ")
    return dough_option


def remove_pizza():
    client_view_cart()
    pizza_id = input("What is the id of the pizza you want to remove? ")
    pizza_exists = is_pizza_in_cart(pizza_id)
    # Checks if Pizza is in cart
    if pizza_exists == "":
        curr_cart.remove_pizza(int(pizza_id))
        print("Pizza removed from cart.")
    else:
        print(pizza_exists)


def edit_size(pizza_id):
    previous_price = 0.0
    curr_price = 0.0
    print("Pizza Sizes: 1 = Small, 2 = Medium, 3 = Large, 4 = Party")
    size = input("What size would you like? ")
    while int(size) not in range(1, 5):
        print("Please enter a valid size number.")
        size = input("What size would you like? ")
    for pizza in curr_cart.pizzas:
        if pizza.id == int(pizza_id):
            previous_price = pizza.price
            pizza.choose_size(int(size))
            pizza.calculate_price()
            curr_price = pizza.price
            curr_cart.update_price(previous_price, curr_price)
    print("Size has been changed.")


def remove_toppings(pizza_id):
    previous_price = 0.0
    curr_price = 0.0
    print("Enter Topping Number: 1: pepperoni, 2:bacon, 3:pineapple, 4:chicken,\n \
                        5: bell peppers, 6: jalapeno peppers")
    print("Enter 0 to Stop Removing Toppings")
    list_of_toppings = ""
    topping_option = -1
    while int(topping_option) != 0:
        topping_option = input(
            "What toppings do you want to remove? ")
        if int(topping_option) in range(1, 7):
            list_of_toppings += str(topping_option) + ","
            print("Topping Removed.")
        elif int(topping_option) == 0:
            list_of_toppings = list_of_toppings[:-1]
        else:
            print(
                "Please enter a valid topping number or press 0 to stop.")
    for pizza in curr_cart.pizzas:
        if pizza.id == int(pizza_id):
            for x in list_of_toppings.split(","):
                previous_price = pizza.price
                pizza.remove_topping(int(x))
                pizza.calculate_price()
                curr_price = pizza.price
                curr_cart.update_price(previous_price, curr_price)
    print("These toppings will not be on your Pizza.")


def edit_toppings(pizza_id):
    previous_price = 0.0
    curr_price = 0.0
    print("Enter Topping Number: 1: pepperoni, 2:bacon, 3:pineapple, 4:chicken,\n \
                        5: bell peppers, 6: jalapeno peppers")
    print("Enter 0 to Stop Adding Toppings")
    list_of_toppings = ""
    topping_option = -1
    while int(topping_option) != 0:
        topping_option = input(
            "What toppings do you want to add? ")
        if int(topping_option) in range(1, 7):
            list_of_toppings += str(topping_option) + ","
            print("Topping added.")
        elif int(topping_option) == 0:
            list_of_toppings = list_of_toppings[:-1]
        else:
            print(
                "Please enter a valid topping number or press 0 to stop.")

    for pizza in curr_cart.pizzas:
        if pizza.id == int(pizza_id):
            for x in list_of_toppings.split(","):
                previous_price = pizza.price
                pizza.add_topping(int(x))
                pizza.calculate_price()
                curr_price = pizza.price
                curr_cart.update_price(previous_price, curr_price)
    return "These toppings will be added to Pizza."


def edit_dough(pizza_id):
    previous_price = 0.0
    curr_price = 0.0
    print(
        "Pizza Dough Number: 1 = White, 2 = Whole Wheat, 3 = Cauliflower")
    dough = input("What dough would you like? ")
    while int(dough) not in range(1, 4):
        print("Please enter a valid dough type number.")
        dough = input("What dough would you like? ")
    for pizza in curr_cart.pizzas:
        if pizza.id == int(pizza_id):
            previous_price = pizza.price
            pizza.choose_dough(int(dough))
            pizza.calculate_price()
            curr_price = pizza.price
            curr_cart.update_price(previous_price, curr_price)
    print("Dough has been changed.")


def view_menu():
    response = requests.get("http://127.0.0.1:5000/view-menu")
    print(response.text + "\n")


def parse_menu():
    order_item = input("What item would you like to look up? ")
    url_string = "http://127.0.0.1:5000/parse-menu/" + order_item
    response = requests.post(url_string)
    print(response.text)


def checkout():
    client_view_cart()
    confirmation = input(
        "Are you sure you want to check out now?(Enter \'yes\' or \'no\') ")
    while confirmation.lower() != "no" and confirmation.lower() != "yes":
        confirmation = input(
            "Are you sure you want to check out now?(Enter \'yes\' or \'no\') ")
    if confirmation.lower() == "no":
        print("Maybe order some more?")
    else:
        choose_delivery_method()
        checkout_complete()
        exit()


def choose_delivery_method():
    cart_status = is_cart_empty()
    if cart_status == "":
        print("Choose Delivery Method:")
        print(
            "1: In-Store Pickup, 2: In-House Delivery, 3: Foodora, 4: Uber-Eats")
        delivery_choice = input(
            "How would you like to get your food? ")
        if int(delivery_choice) == 1:
            print("Your order will be ready for pickup in 20 minutes.")
        else:
            address = input("Enter your address: ")
            if int(delivery_choice) == 2:
                csv_string = csv_generation(address)
                url_string = "http://127.0.0.1:5000/csv-reception/" + csv_string
                response = requests.post(url_string)
                print(response.text)
                print("Order Info sent to Delivery Man in CSV format")
            if int(delivery_choice) == 3:
                csv_string = csv_generation(address)
                url_string = "http://127.0.0.1:5000/csv-reception/" + csv_string
                response = requests.post(url_string)
                print(response.text)
                print("Order Info sent to Foodora in CSV format")
            if int(delivery_choice) == 4:
                url_string = "http://127.0.0.1:5000/json-generation/" + address
                response = requests.post(url_string)
                print(response.text)
                print("Order Info sent to UberEats in JSON format")
    else:
        print(cart_status)


def is_price_float(new_price):
    try:
        float(new_price)
        return True
    except ValueError:
        return False


def is_pizza_in_cart(id):
    for pizza in curr_cart.pizzas:
        if pizza.id == int(id):
            return ""
    return "No such Pizza in cart."


def is_cart_empty():
    if not curr_cart.drinks and not curr_cart.pizzas:
        return "Cart is Empty"
    return ""


def are_there_drinks_in_cart():
    if curr_cart.drinks:
        return ""
    return "No Drinks in Cart"


def client_clear_cart():
    global pizza_id
    pizza_id = 0
    curr_cart.clear_cart()
    print("Cart Cleared")


def client_view_cart():
    print(curr_cart.view_cart())


def client_remove_drinks():
    print("Your current drinks are: ")
    print(curr_cart.get_drinks())
    drink_option = input_drink_name()
    drink_quantity = input_drink_quantity()
    if curr_cart.drinks.get(drink_option.lower()):
        return_string = "Drink removed"
    else:
        return_string = "Invalid drink. Try again."
    curr_cart.remove_drink(drink_option, int(drink_quantity))
    print(return_string)



def client_add_drinks():
    print(curr_cart.view_valid_drinks())
    drink_option = input_drink_name()
    drink_quantity = input_drink_quantity()
    curr_cart.add_drink(drink_option, int(drink_quantity))
    if drink_option.lower() in curr_cart.view_valid_drinks():
        print("Drink added")
    else:
        print("Invalid drink. Try again.")


def input_drink_quantity():
    return input("How many? ")


def input_drink_name():
    return input("What drink would you like? ")

def csv_generation(address):
    csv_string = "Order address:, Order Details for Pizza, Order Details for Price,\
        Order Details for Drinks, Order Number\n"
    if curr_cart.drinks and not curr_cart.pizzas:
        csv_string += address + ", No Pizzas , No Pizza Prices, " + str(curr_cart.drinks) + \
                      " ($1.50 each), " + str(get_cart_id()) + "\n"
        return csv_string
    for pizza in curr_cart.pizzas:
        csv_string += address + ", " + pizza.size + ": " + str(pizza.toppings) + ", " + \
                      str("${:,.2f}".format(pizza.price)) + ", " + str(curr_cart.drinks) + \
                      " ($1.50 each), " + str(get_cart_id()) + "\n"
    return csv_string

def checkout_complete():
    response = requests.get("http://127.0.0.1:5000/complete-order")
    print(response.text)


if __name__ == "__main__":
    main()
