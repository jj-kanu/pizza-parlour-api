from PizzaParlour import *
from ShoppingCart import *
from unittest.mock import patch
from unittest import TestCase
import io
import sys
import unittest

class Test(TestCase):

    def test_pizza(self):
        response = app.test_client().get('/pizza')

        assert response.status_code == 200
        assert response.data == b'Welcome to Pizza Planet!'

    def test_create_cart(self):
        cart = ShoppingCart(1)
        assert cart.order_number == 1
        assert cart.pizzas == []
        assert cart.drinks == {}
        assert cart.total == 0.0
        assert cart.valid_drinks == ["water", "coke", "nestea", "mountain dew", "canada dry"]

    def test_add_drink(self):
        cart=get_cart()
        add_drink_to_cart("water", 1)
        assert cart.drinks == {"water":1}

    def test_add_invalid_drink(self):
        cart=get_cart()
        output = io.StringIO()
        sys.stdout = output
        add_drink_to_cart("pepsi", 1)
        assert cart.drinks == {"water": 1}

    def test_remove_drink(self):
        cart=get_cart()
        add_drink_to_cart("water", 1)
        remove_drink_from_cart("water", 1)
        assert cart.drinks == {"water":0}

    def test_remove_invalid_drink(self):
        cart=get_cart()
        add_drink_to_cart("water", 1)
        remove_drink_from_cart("pepsi", 1)
        assert cart.drinks == {"water":1}

    def test_remove_invalid_quantity_of_drinks(self):
        cart=get_cart()
        add_drink_to_cart("water", 1)
        remove_drink_from_cart("water", 5)
        assert cart.drinks == {"water":2}

    @patch ('builtins.input', return_value = 1)
    def test_add_pizza_to_cart(self, input):
        expected_pizza = Pizza(1,0)
        cart = get_cart()
        choose_pizza(input.return_value)
        assert cart.pizzas[0].id == expected_pizza.id

    @patch('builtins.input', return_value=0)
    def test_remove_pizza_from_cart(self, input):
        cart = get_cart()
        #Reset the pizza array
        cart.pizzas = []
        add_pizza_to_cart(Pizza(1,0))
        remove_pizza_from_cart(input.return_value)
        assert cart.pizzas == []

    @patch('builtins.input', return_value=1)
    def test_invalid_remove_pizza_from_cart(self, input):
        cart = get_cart()
        add_pizza_to_cart(Pizza(1,0))
        old_pizza_array = cart.pizzas.copy()
        remove_pizza_from_cart(input.return_value)
        assert cart.pizzas == old_pizza_array

    @patch ('builtins.input', return_value = 1)
    def test_view_cart(self, input):
        cart = get_cart()
        choose_pizza(input.return_value)
        add_drink_to_cart("water", 1)
        add_drink_to_cart("coke", 2)
        self.assertEqual(get_cart_string(), cart.view_cart())

    def test_clear_cart(self):
        cart = get_cart()
        clear_cart()
        assert cart.pizzas == []
        assert cart.drinks == {}
        assert cart.total == 0.0

    def test_get_drinks_in_cart(self):
        cart = get_cart()
        self.assertEqual(get_drinks_in_cart(), cart.drinks)

    def test_get_drinks_list(self):
        expected_string = "Drinks: water, coke, nestea, mountain dew, canada dry"
        self.assertEqual(get_valid_drinks(), expected_string)

    #Pizza tests
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

    def test_create_pizza_wrong_input(self):
        output = io.StringIO()
        sys.stdout = output
        pizza = Pizza(5, 1)
        sys.stdout = sys.__stdout__
        self.assertEqual(output.getvalue(), "Please enter a valid Pizza type.\n")

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
        output = io.StringIO()
        sys.stdout = output
        pizza = Pizza(4, 1)
        pizza.add_topping(8)
        sys.stdout = sys.__stdout__
        self.assertEqual(output.getvalue(),
                         "Please enter a valid topping option.\n")

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
