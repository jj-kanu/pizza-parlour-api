from PizzaParlour import *
from ShoppingCart import *
from unittest.mock import patch
from unittest import TestCase
import io
import sys
import unittest

def get_input(text):
    return input(text)

def pick_pizza():
    ans = get_input("What pizza?")
    if ans == ("1"):
        myPizza = Pizza(1,1)
    return myPizza

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

    def test_view_cart(self):
        cart = get_cart()
        add_drink_to_cart("water", 1)
        add_drink_to_cart("coke", 2)
        output = io.StringIO()
        sys.stdout = output
        cart.view_cart()
        sys.stdout = sys.__stdout__
        assert output.getvalue() == "('Drinks in cart:' 'water : 1'"
