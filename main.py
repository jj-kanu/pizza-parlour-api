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
    return input("1 to add a pizza, 2 to add a drink, 3 to remove a drink, 4 to view cart, \
        5 to clear cart, 6 to view menu, 7 to look up menu item. 0 to exit: ")


def accept_input(main_menu_input):
    if main_menu_input == "1":
        print(
            "Enter 1 for Pepperoni, 2 for Cheese, 3 for Meat Lover's, 4 for Custom Pizza.")
        pizza_option = input("What type of pizza would you like?")
        while pizza_option not in range(1, 5):
            print("Invalid pizza type. Please enter a valid pizza type.")
            pizza_option = input("What type of pizza would you like?")
        # PREMADE PIZZAS
        if pizza_option in range(1, 4):
            print("Enter 1 for Small, 2 for Medium, 3 for Large, 4 for Party Size.")
            size_option = input("What size pizza do you want?")
            while size_option not in range(1, 5):
                print("Invalid size. Please enter a valid pizza size flag.")
                size_option = input("What size pizza do you want?")
            url_string = "http://127.0.0.1:5000/choose-pizza/" + \
                pizza_option + "/" + size_option
            response = requests.post(url_string)
            print("Pizza added to cart.")
        # CUSTOM PIZZAS
        elif(pizza_option == 4):
            # Dough
            print("Enter 1 for White, 2 for Whole Wheat, 3 for Cauliflower")
            dough_option = input("What type of dough would you like?")
            while dough_option not in range(1, 4):
                print("Invalid dough type. Please enter a valid dough type flag.")
                dough_option = input("What type of dough would you like?")
            # Toppings
            print("Enter Topping Number: 1: pepperoni, 2:bacon, 3:pineapple, 4:pineapples, 5:chicken,\n \
                6: bell peppers, 7: jalapeno peppers")
            print("Enter 0 to Stop Adding Toppings")
            list_of_toppings = ""
            topping_option = -1
            while topping_option != 0:
                topping_option = input("What toppings do you want to add?")
                if topping_option in range(1, 8):
                    list_of_toppings += str(topping_option) + ","
                    print("Topping added.")
                else:
                    print("Please enter a topping number or press 0 to stop.")
            # Size
            print("Enter 1 for Small, 2 for Medium, 3 for Large, 4 for Party Size.")
            size_option = input("What size pizza do you want?")
            while size_option not in range(1, 5):
                print("Invalid size. Please enter a valid pizza size flag.")
                size_option = input("What size pizza do you want?")

            url_string = "http://127.0.0.1:5000/create-pizza/" + \
                dough_option + "/" + list_of_toppings + "/" + size_option
            response = requests.post(url_string)
            print(response.text)

    # Edit Pizza
    if main_menu_input == "9":
        response = requests.get("http://127.0.0.1:5000/cart-string")
        print(response.text)

        pizza_id = input("What is the id of the pizza you want to edit?")
        url_string = "http://127.0.0.1:5000/is-pizza-in-cart/" + pizza_id
        response = requests.post(url_string)
        if not response:
            print("No such Pizza in cart.")

    # Extract this out to helper functions
    if main_menu_input == "2":
        url_string = client_add_drinks()
        response = requests.post(url_string)
        print(response.text)

    if main_menu_input == "3":
        response = requests.get("http://127.0.0.1:5000/drinks-in-cart")
        print(response.text)
        url_string = client_remove_drinks()
        response = requests.post(url_string)
        print(response.text)

    if main_menu_input == "4":
        client_view_cart()

    if main_menu_input == "5":
        client_clear_cart()

    if main_menu_input == "6":
        response = requests.get("http://127.0.0.1:5000/view-menu")
        for line in response:
            print(line)

    if main_menu_input == "7":
        order_item = input("What item would you like to look up?")
        url_string = "http://127.0.0.1:5000/parse-menu/" + order_item
        response = requests.post(url_string)
        print(response.text)

    return main_menu_input


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
