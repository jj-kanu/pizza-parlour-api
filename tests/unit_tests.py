from PizzaParlour import *
from ShoppingCart import *
from unittest.mock import patch
import io
import sys
import unittest

def test_pizza():
    response = app.test_client().get('/pizza')

    assert response.status_code == 200
    assert response.data == b'Welcome to Pizza Planet!'

def test_create_cart():
    cart = ShoppingCart(1)
    assert cart.order_number == 1
    assert cart.pizzas == []
    assert cart.drinks == {}
    assert cart.total == 0.0
    assert cart.valid_drinks == ["water", "coke", "nestea", "mountain dew", "canada dry"]

def test_add_drink():
    cart=get_cart()
    add_drink_to_cart("water", 1)
    assert cart.drinks == {"water":1}

def test_add_invalid_drink():
    cart=get_cart()
    output = io.StringIO()
    sys.stdout = output
    add_drink_to_cart("pepsi", 1)
    assert cart.drinks == {"water": 1}

def test_remove_drink():
    cart=get_cart()
    remove_drink_from_cart("water", 1)
    assert cart.drinks == {"water":0}

def test_remove_invalid_drink():
    cart=get_cart()
    add_drink_to_cart("water", 1)
    remove_drink_from_cart("pepsi", 1)
    assert cart.drinks == {"water":1}

def test_remove_invalid_quantity_of_drinks():
    cart=get_cart()
    add_drink_to_cart("water", 1)
    remove_drink_from_cart("water", 5)
    assert cart.drinks == {"water":2}

def test_add_pizza_to_cart():
    choose_pizza(1)
    with unittest.mock.patch('builtins.input', return_value=1):
        cart = get_cart()
        assert cart.pizzas == [1]

def test_view_cart():
    cart = get_cart()
    add_drink_to_cart("water", 1)
    add_drink_to_cart("coke", 2)
    output = io.StringIO()
    sys.stdout = output
    cart.view_cart()
    sys.stdout = sys.__stdout__
    assert output.getvalue() == "('Drinks in cart:' 'water : 1'"
