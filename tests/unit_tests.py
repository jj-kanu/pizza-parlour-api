from PizzaParlour import *
from ShoppingCart import *
from main import *
from unittest.mock import patch
from unittest import TestCase
import io
import sys
import unittest


class Test(TestCase):

    # Pizza Parlour Client-Called-Functions Tests --------------------------------
    def test_is_pizza_in_cart(self):
        cart = ShoppingCart(0)
        response = app.test_client().get('/is-pizza-in-cart/0')

        assert response.status_code == 200
        assert response.data == b"No such Pizza in cart."

        pizza = Pizza(1, 0)
        cart.add_pizza(pizza)
        response2 = app.test_client().get('/is-pizza-in-cart/0')
        assert response2.status_code == 200
        assert response2.data

    def test_is_cart_empty(self):
        cart = ShoppingCart(0)
        response = app.test_client().get('/is-cart-empty')
        assert response.status_code == 200
        assert response.data == b"Cart is Empty"

        pizza = Pizza(1, 0)
        cart.add_pizza(pizza)
        response2 = app.test_client().get('/is-cart-empty')
        assert response2.status_code == 200
        assert response2.data

    def test_view_menu(self):
        menu = open('Menu.txt', 'r').read()
        response = app.test_client().get('/view-menu')
        assert response.status_code == 200
        self.assertEqual(response.data.decode('utf-8'), menu)

    def test_parse_menu(self):
        response = app.test_client().get('/parse-menu/fail')
        assert response.status_code == 200
        assert response.data == b"This item isn't recognized. Perhaps view full menu to check?"
        response2 = app.test_client().get('/parse-menu/pepperoni')
        assert response2.status_code == 200
        assert response2.data == b"This item is a possible topping for a pizza. \n \
            One topping is on the house, additional toppings are $1 each."
        response3 = app.test_client().get('/parse-menu/pepperoni pizza')
        assert response3.status_code == 200
        assert response3.data == b"One of the Kanuli specials. Made on White Bread Dough \n \
            (S: 9/ M: 11/ L: 13/ P: 18)"
        response4 = app.test_client().get('/parse-menu/cheese')
        assert response4.status_code == 200
        assert response4.data == b"Cheese is automatically applied to all pizzas. It's on the house."
        response5 = app.test_client().get('/parse-menu/white')
        assert response5.status_code == 200
        assert response5.data == b"This item is a possible dough base for a pizza.\
            (White: 3/ WW: 3.50/ Cauliflower: 4)"
        response6 = app.test_client().get('/parse-menu/pizza')
        assert response6.status_code == 200
        assert response6.data == b"Yup, that's what we serve. You can make your own or get a special.\n \
                Prices may vary based on size, dough, and number of toppings."

    @patch('builtins.input', return_value=1)
    def test_choose_pizza(self, input):
        expected_pizza = Pizza(1, 0)
        expected_pizza.size = "Medium"
        cart = get_cart()
        url_string = "/choose-pizza/" + str(input.return_value) + "/2"
        response = app.test_client().get(url_string)
        assert cart.pizzas[0].id == expected_pizza.id
        assert cart.pizzas[0].size == expected_pizza.size
        assert response.status_code == 200
        assert response.data == b"Pizza added to cart."

    def test_create_pizza(self):
        expected_pizza = Pizza(4, 0)
        expected_pizza.size = "Medium"
        expected_pizza.dough = "Cauliflower"
        expected_pizza.toppings = {1: "pepperoni", 2: "bacon", 3: "pineapples"}
        cart = get_cart()
        response = app.test_client().get("/create-pizza/3/1,2,3/2")
        assert cart.pizzas[0].id == expected_pizza.id
        assert cart.pizzas[0].size == expected_pizza.size
        assert cart.pizzas[0].dough == expected_pizza.dough
        assert cart.pizzas[0].toppings == expected_pizza.toppings
        assert response.status_code == 200
        assert response.data == b"Pizza added to cart."

    def test_change_pizza_dough(self):
        cart = get_cart()
        pizza = Pizza(1, 0)
        cart.add_pizza(pizza)
        assert cart.pizzas[0].dough == "White"
        response = app.test_client().get("/change-pizza-dough/0/3")
        assert cart.pizzas[0].dough == "Cauliflower"
        assert response.status_code == 200
        assert response.data == b"Dough has been changed."

    def test_server_change_pizza_size(self):
        cart = get_cart()
        pizza = Pizza(1, 0)
        pizza.size = "Small"
        cart.add_pizza(pizza)
        assert cart.pizzas[0].size == "Small"
        response = app.test_client().get("/change-pizza-size/0/4")
        assert cart.pizzas[0].size == "Party Size"
        assert response.status_code == 200
        assert response.data == b"Size has been changed."

    def test_server_add_toppings_to_pizza(self):
        cart = get_cart()
        pizza = Pizza(1, 0)
        pizza.size = "Small"
        cart.add_pizza(pizza)
        assert cart.pizzas[0].toppings == {1: "pepperoni"}
        response = app.test_client().get("add-topping-to-pizza/0/2,3")
        assert cart.pizzas[0].toppings == {
            1: "pepperoni", 2: "bacon", 3: "pineapples"}
        assert response.status_code == 200
        assert response.data == b"These toppings will be added to Pizza."

    def test_server_remove_topping_from_pizza(self):
        cart = get_cart()
        pizza = Pizza(3, 0)
        pizza.size = "Small"
        cart.add_pizza(pizza)
        assert cart.pizzas[0].toppings == {
            1: "pepperoni", 2: "bacon", 4: "chicken"}
        response = app.test_client().get("remove-topping-from-pizza/0/1,2,3,4,5,6")
        assert cart.pizzas[0].toppings == {}
        assert response.status_code == 200
        assert response.data == b"These toppings will not be on your Pizza."

    def test_edit_pizza_price(self):
        cart = get_cart()
        pizza = Pizza(3, 0)
        pizza.size = "Small"
        pizza.calculate_price()
        cart.add_pizza(pizza)
        assert cart.pizzas[0].price == 11
        response = app.test_client().get("edit-pizza-price/0/9.87")
        assert cart.pizzas[0].price == 9.87
        assert response.status_code == 200
        assert response.data == b"Price of Pizza 0 has been changed to $9.87"

    def test_csv_generation(self):
        cart = get_cart()
        add_drink_to_cart("water", 1)
        response = app.test_client().get("csv-generation/123 sesame street")
        assert response.status_code == 200
        assert response.data
        pizza = Pizza(3, 0)
        pizza.size = "Small"
        pizza.calculate_price()
        cart.add_pizza(pizza)
        response2 = app.test_client().get("csv-generation/123 sesame street")
        assert response2.status_code == 200
        assert response2.data

    # Shopping Cart Tests -------------------------------------------------------
    def test_pizza(self):
        response = app.test_client().get('/pizza')

        assert response.status_code == 200
        assert response.data == b'Welcome to Kanuli\'s Pizza!'

    def test_create_cart(self):
        cart = ShoppingCart(1)
        assert cart.order_number == 1
        assert cart.pizzas == []
        assert cart.drinks == {}
        assert cart.total == 0.0
        assert cart.valid_drinks == [
            "water", "coke", "nestea", "mountain dew", "canada dry"]

    def test_add_drink(self):
        cart = get_cart()
        add_drink_to_cart("water", 1)
        assert cart.drinks == {"water": 1}

    def test_add_invalid_drink(self):
        cart = get_cart()
        output = io.StringIO()
        sys.stdout = output
        add_drink_to_cart("pepsi", 1)
        assert cart.drinks == {"water": 1}

    def test_remove_drink(self):
        cart = get_cart()
        add_drink_to_cart("water", 1)
        remove_drink_from_cart("water", 1)
        assert cart.drinks == {"water": 0}

    def test_remove_invalid_drink(self):
        cart = get_cart()
        add_drink_to_cart("water", 1)
        remove_drink_from_cart("pepsi", 1)
        assert cart.drinks == {"water": 1}

    def test_remove_invalid_quantity_of_drinks(self):
        cart = get_cart()
        add_drink_to_cart("water", 1)
        remove_drink_from_cart("water", 5)
        assert cart.drinks == {"water": 2}

    @patch('builtins.input', return_value=1)
    def test_add_pizza_to_cart(self, input):
        expected_pizza = Pizza(1, 0)
        expected_pizza.size = "Medium"
        cart = get_cart()
        choose_pizza(input.return_value, 2)
        assert cart.pizzas[0].id == expected_pizza.id
        assert cart.pizzas[0].size == expected_pizza.size

    @patch('builtins.input', return_value=0)
    def test_remove_pizza_from_cart(self, input):
        cart = get_cart()
        # Reset the pizza array
        cart.pizzas = []
        add_pizza_to_cart(Pizza(1, 0))
        remove_pizza_from_cart(input.return_value)
        assert cart.pizzas == []

    @patch('builtins.input', return_value=1)
    def test_invalid_remove_pizza_from_cart(self, input):
        cart = get_cart()
        add_pizza_to_cart(Pizza(1, 0))
        old_pizza_array = cart.pizzas.copy()
        remove_pizza_from_cart(input.return_value)
        assert cart.pizzas == old_pizza_array

    @patch('builtins.input', return_value=1)
    def test_view_cart(self, input):
        cart = get_cart()
        choose_pizza(input.return_value, 2)
        add_drink_to_cart("water", 1)
        add_drink_to_cart("coke", 2)
        self.assertEqual(get_cart_string(), cart.view_cart())

    def test_clear_cart(self):
        cart = get_cart()
        clear_cart()
        assert cart.pizzas == []
        assert cart.drinks == {}
        assert cart.total == 0.0

    def test_update_cart_price(self):
        cart = get_cart()
        clear_cart()
        custom_pizza = Pizza(3, 2)
        custom_pizza.size = "Small"
        custom_pizza.calculate_price()
        cart.add_pizza(custom_pizza)
        add_topping_to_pizza(2, "3")
        custom_pizza.calculate_price()
        assert cart.total == 12

    def test_get_drinks_in_cart(self):
        cart = get_cart()
        self.assertEqual(get_drinks_in_cart(), cart.drinks)

    def test_get_drinks_list(self):
        expected_string = "Drinks: water, coke, nestea, mountain dew, canada dry"
        self.assertEqual(get_valid_drinks(), expected_string)

    # Pizza tests ------------------------------------------------------------
    # CREATION TESTS
    def test_default_pepperoni(self):
        pizza = Pizza(1, 1)
        self.assertEqual(pizza.id, 1)
        self.assertEqual(pizza.dough, "White")
        self.assertEqual(pizza.toppings, {1: "pepperoni"})

    def test_default_cheese(self):
        pizza = Pizza(2, 1)
        self.assertEqual(pizza.id, 1)
        self.assertEqual(pizza.dough, "White")
        self.assertEqual(pizza.toppings, {})

    def test_default_meat_lovers(self):
        pizza = Pizza(3, 1)
        self.assertEqual(pizza.id, 1)
        self.assertEqual(pizza.dough, "White")
        self.assertEqual(pizza.toppings, {
            1: "pepperoni", 2: "bacon", 4: "chicken"})

    def test_default_custom(self):
        pizza = Pizza(4, 1)
        self.assertEqual(pizza.id, 1)
        self.assertEqual(pizza.dough, "")
        self.assertEqual(pizza.toppings, {})

        # add_topping TESTS

    def test_add_topping_to_default_pizza(self):
        pizza = Pizza(1, 1)
        pizza.add_topping(4)
        self.assertEqual(pizza.toppings, {1: "pepperoni", 4: "chicken"})

    def test_add_topping_already_on_pizza(self):
        pizza = Pizza(1, 1)
        pizza.add_topping(1)
        self.assertEqual(pizza.toppings, {1: "pepperoni"})

    def test_add_topping_wrong_input(self):
        pizza = Pizza(4, 1)
        old_toppings = pizza.toppings.copy()
        pizza.add_topping(8)
        self.assertEqual(pizza.toppings,
                         old_toppings)

        # remove_topping TESTS

    def test_topping_removed(self):
        pizza = Pizza(3, 1)
        pizza.remove_topping(2)
        self.assertEqual(pizza.toppings, {1: "pepperoni", 4: "chicken"})

    def test_no_topping_removed_given_wrong_flag(self):
        pizza = Pizza(3, 1)
        pizza.remove_topping(3)
        self.assertEqual(pizza.toppings, {
            1: "pepperoni", 2: "bacon", 4: "chicken"})

        # choose_dough TESTS

    def test_change_dough_on_pizza(self):
        pizza = Pizza(1, 1)
        pizza.choose_dough(2)
        self.assertEqual(pizza.dough, "Whole Wheat")

    def test_choose_dough_on_new_custom_pizza(self):
        pizza = Pizza(4, 1)
        pizza.choose_dough(3)
        self.assertEqual(pizza.dough, "Cauliflower")

        # choose_size TESTS

    def test_change_pizza_size(self):
        pizza = Pizza(1, 1)
        pizza.choose_size(1)
        self.assertEqual(pizza.size, "Small")

    def test_set_new_custom_pizza_size(self):
        pizza = Pizza(4, 1)
        pizza.choose_size(4)
        self.assertEqual(pizza.size, "Party Size")

        # calculate_price TESTS

    def test_price_calculated_default_pizza(self):
        pizza = Pizza(3, 1)
        pizza.choose_size(2)
        pizza.calculate_price()
        self.assertEqual(pizza.price, 13)

    def test_cheese_pizza_no_added_topping_cost(self):
        pizza = Pizza(2, 1)
        pizza.choose_size(2)
        pizza.calculate_price()
        self.assertEqual(pizza.price, 11)

    def test_price_calculated_custom_pizza(self):
        pizza = Pizza(4, 1)
        pizza.choose_dough(3)
        pizza.choose_size(4)
        for i in range(1, 7):
            pizza.add_topping(i)
        pizza.calculate_price()
        self.assertEqual(pizza.price, 24)
