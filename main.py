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
    return input("1 to add a pizza, 2 to add a drink, 3 to remove a drink, 4 to view cart, 5 to clear cart, 0 to exit: ")

def accept_input(main_menu_input):
    if main_menu_input == "2":
        response = requests.get("http://127.0.0.1:5000/valid-drinks")
        print(response.text)
        drink_option = input("What drink would you like? ")
        drink_quantity = input("How many? ")
        url_string = "http://127.0.0.1:5000/add-drink/" + drink_option + "/" + drink_quantity
        response = requests.post(url_string)
        print(response.text)

    if main_menu_input == "3":
        response = requests.get("http://127.0.0.1:5000/drinks-in-cart")
        print(response.text)
        drink_option = input("What drink would you like to remove? ")
        drink_quantity = input("How many? ")
        url_string = "http://127.0.0.1:5000/remove-drink/" + drink_option + "/" + drink_quantity
        response = requests.post(url_string)
        print(response.text)

    if main_menu_input == "4" :
        response = requests.get("http://127.0.0.1:5000/cart-string")
        print(response.text)

    if main_menu_input == "5":
        response = requests.get("http://127.0.0.1:5000/clear-cart")
        print(response.text)
    return main_menu_input


if __name__ == "__main__":
    main()