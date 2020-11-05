from Pizza import *
import unittest
import sys


class TestPizza(unittest.TestCase):

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
        output = StringIO.StringIO()
        sys.stdout = output
        pizza = Pizza(5, 1)
        sys.stdout = sys.__stdout__
        self.assertEqual(output.getvalue(), "Please enter a valid Pizza type.")

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
        output = StringIO.StringIO()
        sys.stdout = output
        pizza = Pizza(5, 1)
        sys.stdout = sys.__stdout__
        self.assertEqual(output.getvalue(),
                         "Please enter a valid topping option.")

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
