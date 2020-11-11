import sys
import requests


def main():
    response = requests.get("http://127.0.0.1:5000/pizza")
    print(response.text)
    main_menu_input = main_menu_prompt()
    while accept_input(main_menu_input) != '0':
        main_menu_input = main_menu_prompt()
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
            print("Enter 1 for Small, 2 for Medium, 3 for Large, 4 for Party Size.")
            size_option = input("What size pizza do you want? ")
            while int(size_option) not in range(1, 5):
                print("Invalid size. Please enter a valid pizza size flag.")
                size_option = input("What size pizza do you want? ")
            url_string = "http://127.0.0.1:5000/choose-pizza/" + \
                pizza_option + "/" + size_option
            response = requests.post(url_string)
            print("Pizza added to cart.")
        # CUSTOM PIZZAS
        elif int(pizza_option) == 4:
            # Dough
            print("Enter 1 for White, 2 for Whole Wheat, 3 for Cauliflower")
            dough_option = input("What type of dough would you like? ")
            while int(dough_option) not in range(1, 4):
                print("Invalid dough type. Please enter a valid dough type flag.")
                dough_option = input("What type of dough would you like? ")
            # Toppings
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
            # Size
            print("Enter 1 for Small, 2 for Medium, 3 for Large, 4 for Party Size.")
            size_option = input("What size pizza do you want? ")
            while int(size_option) not in range(1, 5):
                print("Invalid size. Please enter a valid pizza size flag.")
                size_option = input("What size pizza do you want? ")

            url_string = "http://127.0.0.1:5000/create-pizza/" + \
                dough_option + "/" + list_of_toppings + "/" + size_option
            response = requests.post(url_string)
            print(response.text)

    # Remove Pizza
    if main_menu_input == "2":
        client_view_cart()

        pizza_id = input("What is the id of the pizza you want to remove? ")
        url_string = "http://127.0.0.1:5000/is-pizza-in-cart/" + pizza_id
        response = requests.post(url_string)
        # Checks if Pizza is in cart
        if response.text == "":
            url_string = "http://127.0.0.1:5000/remove-pizza/" + pizza_id
            requests.post(url_string)
            print("Pizza removed from cart.")
        else:
            print(response.text)

    # Edit Pizza
    if main_menu_input == "3":
        client_view_cart()

        pizza_id = input("What is the id of the pizza you want to edit? ")
        url_string = "http://127.0.0.1:5000/is-pizza-in-cart/" + pizza_id
        response = requests.post(url_string)
        # Checks if Pizza is in cart
        if response.text == "":
            edit_flag = -1
            while int(edit_flag) != 0:
                print(
                    "Edit Pizza: 1 = Change Dough, 2 = Add Toppings, 3 = Remove Toppings, 4 = Change Size\n\
                        Enter 0 to confirm changes and return to menu.")
                edit_flag = input(
                    "What would you like to change about your pizza? ")
                # Edit Dough
                if int(edit_flag) == 1:
                    print(
                        "Pizza Dough Number: 1 = White, 2 = Whole Wheat, 3 = Cauliflower")
                    dough = input("What dough would you like? ")
                    while int(dough) not in range(1, 4):
                        print("Please enter a valid dough type number.")
                        dough = input("What dough would you like? ")
                    url_string = "http://127.0.0.1:5000/change-pizza-dough/" + pizza_id + "/" + dough
                    response = requests.post(url_string)
                    print(response.text)
                # Add Toppings
                elif int(edit_flag) == 2:
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
                    url_string = "http://127.0.0.1:5000/add-topping-to-pizza/" + \
                        pizza_id + "/" + list_of_toppings
                    response = requests.post(url_string)
                    print(response.text)

                # Remove Toppings
                elif int(edit_flag) == 3:
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
                    url_string = "http://127.0.0.1:5000/remove-topping-from-pizza/" + \
                        pizza_id + "/" + list_of_toppings
                    response = requests.post(url_string)
                    print(response.text)

                    # remove Toppings
                elif int(edit_flag) == 4:
                    print("Pizza Sizes: 1 = Small, 2 = Medium, 3 = Large, 4 = Party")
                    size = input("What size would you like? ")
                    while int(size) not in range(1, 5):
                        print("Please enter a valid size number.")
                        size = input("What size would you like? ")
                    url_string = "http://127.0.0.1:5000/change-pizza-size/" + pizza_id + "/" + size
                    response = requests.post(url_string)
                    print(response.text)
                else:
                    print(
                        "Please pick a valid edit option or enter 0 to go back to menu.")
        else:
            print(response.text)

    # Extract this out to helper functions
    if main_menu_input == "4":
        url_string = client_add_drinks()
        response = requests.post(url_string)
        print(response.text)

    if main_menu_input == "5":
        response = requests.get("http://127.0.0.1:5000/drinks-in-cart")
        print(response.text)
        url_string = client_remove_drinks()
        response = requests.post(url_string)
        print(response.text)

    if main_menu_input == "6":
        client_view_cart()

    if main_menu_input == "7":
        client_clear_cart()

    if main_menu_input == "8":
        response = requests.get("http://127.0.0.1:5000/view-menu")
        print(response.text + "\n")

    if main_menu_input == "9":
        order_item = input("What item would you like to look up? ")
        url_string = "http://127.0.0.1:5000/parse-menu/" + order_item
        response = requests.post(url_string)
        print(response.text)

    if main_menu_input == "10":
        client_view_cart()
        confirmation = input(
            "Are you sure you want to check out now?(Enter \'yes\' or \'no\') ")
        while confirmation.lower() != "no" and confirmation.lower() != "yes":
            confirmation = input(
                "Are you sure you want to check out now?(Enter \'yes\' or \'no\') ")
        if confirmation.lower() == "no":
            print("Maybe order some more?")
        else:
            response = requests.get("http://127.0.0.1:5000/is-cart-empty")
            if response.text == "":
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
                        url_string = "http://127.0.0.1:5000/csv-generation/" + address
                        response = requests.post(url_string)
                        print(response.text)
                        print("Order Info sent to Delivery Man in CSV format")
                    if int(delivery_choice) == 3:
                        url_string = "http://127.0.0.1:5000/csv-generation/" + address
                        response = requests.post(url_string)
                        print(response.text)
                        print("Order Info sent to Foodora in CSV format")
                    if int(delivery_choice) == 4:
                        url_string = "http://127.0.0.1:5000/json-generation/" + address
                        response = requests.post(url_string)
                        print(response.text)
                        print("Order Info sent to UberEats in JSON format")
            else:
                print(response.text)

    if main_menu_input == "98":
        client_view_cart()

        pizza_id = input(
            "What is the id of the pizza you want to change price? ")
        url_string = "http://127.0.0.1:5000/is-pizza-in-cart/" + pizza_id
        response = requests.post(url_string)
        # Checks if Pizza is in cart
        if response.text == "":
            new_price = input("What is this pizza's new price? $")
            while not is_price_float(new_price):
                new_price = input(
                    "What is this pizza's new price?(Enter in dollars) $")
            if float(new_price) < 0:
                print("This is an invalid price. Price will not be changed")
                return
            url_string = "http://127.0.0.1:5000/edit-pizza-price/" + pizza_id + "/" + new_price
            response = requests.post(url_string)
            print(response.text)
        else:
            print(response.text)

    if main_menu_input == "99":
        client_view_cart()
        response = requests.post(
            "http://127.0.0.1:5000/are-there-drinks-in-cart")
        if response.text == "":
            # Do stuff
            return
        else:
            print(response.text)
    return main_menu_input


def is_price_float(new_price):
    try:
        float(new_price)
        return True
    except ValueError:
        return False


def client_clear_cart():
    response = requests.get("http://127.0.0.1:5000/clear-cart")
    print(response.text)


def client_view_cart():
    response = requests.get("http://127.0.0.1:5000/cart-string")
    print(response.text)


def client_remove_drinks():
    drink_option = input("What drink would you like to remove? ")
    drink_quantity = input("How many? ")
    url_string = "http://127.0.0.1:5000/remove-drink/" + \
        drink_option + "/" + drink_quantity
    return url_string


def client_add_drinks():
    response = requests.get("http://127.0.0.1:5000/valid-drinks")
    print(response.text)
    drink_option = input("What drink would you like? ")
    drink_quantity = input("How many? ")
    url_string = "http://127.0.0.1:5000/add-drink/" + \
        drink_option + "/" + drink_quantity
    return url_string


if __name__ == "__main__":
    main()
