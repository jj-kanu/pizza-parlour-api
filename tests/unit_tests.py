from unittest import TestCase
from unittest.mock import patch

from PizzaParlour import *
from main import *


class Test(TestCase):

    # Pizza Parlour Client-Called-Functions Tests --------------------------------

    @patch('builtins.input')
    def test_main_menu_prompt(self, input):
        input.side_effect = ['1']
        assert main_menu_prompt() == '1'

    def test_float_check_true(self):
        assert is_price_float(12.00) == True

    def test_float_check_false(self):
        assert is_price_float("12ab") == False

    def test_is_pizza_in_cart(self):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        pizza = Pizza(1, 0)
        cart.add_pizza(pizza)
        result = is_pizza_in_cart(0)
        assert result == ""

    @patch('builtins.input')
    def test_remove_drinks_through_cli(self, input):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        cart.add_drink("water", 5)
        input.side_effect = ['water', 2]
        accept_input('5')
        assert cart.drinks == {'water': 3}

    def test_is_cart_empty(self):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        assert get_client_cart().pizzas == []
        assert cart.drinks == {}
        assert cart.total == 0.0
        assert is_cart_empty() == "Cart is Empty"

    def test_no_drinks_in_cart(self):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        assert get_client_cart().pizzas == []
        assert cart.drinks == {}
        assert cart.total == 0.0
        assert are_there_drinks_in_cart() == "No Drinks in Cart"

    def test_no_pizzas_in_cart(self):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        assert get_client_cart().pizzas == []
        assert cart.drinks == {}
        assert cart.total == 0.0
        assert is_pizza_in_cart(50) == "No such Pizza in cart."

    def test_is_cart_is_not_empty(self):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        cart.add_drink("water", 2)
        cart.edit_drinks_price(2)
        assert get_client_cart().pizzas == []
        assert cart.drinks == {"water": 2}
        assert cart.total == 4.0
        assert is_cart_empty() == ""

    def test_clear_cart_through_input(self):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        cart.add_drink("water", 2)
        accept_input("7")
        assert cart.drinks == {}

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
        response7 = app.test_client().get('/parse-menu/cheese pizza')
        assert response7.status_code == 200
        assert response7.data == b"One of the Kanuli specials. Made on White Bread Dough \n \
            (S: 9/ M: 11/ L: 13/ P: 18)"
        response8 = app.test_client().get('/parse-menu/meat lover\'s pizza')
        assert response8.status_code == 200
        assert response8.data == b"One of the Kanuli specials. Made on White Bread Dough \n \
            (S: 11/ M: 13/ L: 15/ P: 20)"

    @patch('builtins.input')
    def test_instore_pickup(self, input):
        input.side_effect = ["1"]
        assert choose_delivery_method() == "Your order will be ready for pickup in 20 minutes."


    @patch('builtins.input')
    def test_choose_pizza(self, input):
        expected_pizza = Pizza(1, 0)
        expected_pizza.size = "Medium"
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        input.side_effect = ['1', '2']
        accept_input("1")

        assert cart.pizzas[0].id == expected_pizza.id
        assert cart.pizzas[0].size == expected_pizza.size

    @patch('builtins.input')
    def test_choose_pizza_size(self, input):
        input.side_effect = ['10', '2']
        assert choose_pizza_size() == '2'


    def test_create_pizza(self):
        expected_pizza = Pizza(4, 0)
        expected_pizza.size = "Medium"
        expected_pizza.dough = "Cauliflower"
        expected_pizza.toppings = {1: "pepperoni", 2: "bacon", 3: "pineapples"}
        set_cart(1)
        cart = get_client_cart()
        client_clear_cart()
        custom_pizza_creation(3,"1,2,3",2)
        assert cart.pizzas[0].id == expected_pizza.id
        assert cart.pizzas[0].size == expected_pizza.size
        assert cart.pizzas[0].dough == expected_pizza.dough
        assert cart.pizzas[0].toppings == expected_pizza.toppings

    @patch('builtins.input')
    def test_create_custom_pizza(self, input):
        expected_pizza = Pizza(4, 0)
        expected_pizza.size = "Medium"
        expected_pizza.dough = "Cauliflower"
        expected_pizza.toppings = {1: "pepperoni", 2: "bacon", 3: "pineapples"}
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        input.side_effect = ['4', '3', '1' , '2', '3', '0', '2']
        accept_input("1")
        assert cart.pizzas[0].id == expected_pizza.id
        assert cart.pizzas[0].size == expected_pizza.size
        assert cart.pizzas[0].dough == expected_pizza.dough
        assert cart.pizzas[0].toppings == expected_pizza.toppings

    @patch('builtins.input')
    def test_change_pizza_dough(self, input):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        pizza = Pizza(1, 0)
        cart.add_pizza(pizza)
        assert cart.pizzas[0].dough == "White"
        input.side_effect = ['0', '1', '3', '0']
        accept_input("3")
        assert cart.pizzas[0].dough == "Cauliflower"

    @patch('builtins.input')
    def test_server_change_pizza_size(self, input):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        pizza = Pizza(1, 0)
        pizza.size = "Small"
        cart.add_pizza(pizza)
        assert cart.pizzas[0].size == "Small"
        input.side_effect = ['0','4', '4', '0']
        accept_input("3")
        assert cart.pizzas[0].size == "Party Size"


    @patch('builtins.input')
    def test_server_add_toppings_to_pizza(self, input):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        pizza = Pizza(1, 0)
        pizza.size = "Small"
        cart.add_pizza(pizza)
        assert cart.pizzas[0].toppings == {1: "pepperoni"}
        input.side_effect= ['0', '2', '2','3','0','0']
        accept_input("3")
        assert cart.pizzas[0].toppings == {
            1: "pepperoni", 2: "bacon", 3: "pineapples"}


    @patch('builtins.input')
    def test_server_remove_topping_from_pizza(self, input):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        pizza = Pizza(3, 0)
        pizza.size = "Small"
        cart.pizzas=[pizza]
        input.side_effect = ['0', '3', '1', '2', '4', '0', '0']
        assert cart.pizzas[0].toppings == {
            1: "pepperoni", 2: "bacon", 4: "chicken"}
        accept_input("3")
        assert cart.pizzas[0].toppings == {}

    @patch('builtins.input')
    def test_edit_pizza_price(self,input):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        pizza = Pizza(3, 0)
        pizza.size = "Small"
        pizza.calculate_price()
        cart.add_pizza(pizza)
        assert cart.pizzas[0].price == 11
        input.side_effect = ['0', '9.87']
        accept_input("98")

        assert cart.pizzas[0].price == 9.87

    @patch('builtins.input')
    def test_edit_invalid_pizza_price(self, input):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        pizza = Pizza(3, 0)
        pizza.size = "Small"
        pizza.calculate_price()
        cart.add_pizza(pizza)
        assert cart.pizzas[0].price == 11
        input.side_effect = ['0', '-1.25']
        accept_input("98")

        assert cart.pizzas[0].price == 11

    @patch('builtins.input')
    def test_edit_drinks_price(self, input):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        cart.add_drink("water", 5)
        assert (cart.drinks.get("water") * 1.5) == 7.50
        input.side_effect = ['2']
        accept_input("99")

        assert cart.total == 10.0

    @patch('builtins.input')
    def test_edit_drinks_price_invalid(self, input):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        cart.add_drink("water", 5)
        assert (cart.drinks.get("water") * 1.5) == 7.50
        input.side_effect = ['-5.0']
        accept_input("99")

        assert cart.total == 10

    # Shopping Cart Tests -------------------------------------------------------
    def test_pizza(self):
        response = app.test_client().get('/pizza')

        assert response.status_code == 200
        assert response.data == b'Welcome to Kanuli\'s Pizza!'

    def test_cart_id(self):
        response = app.test_client().get('/cart')

        assert response.status_code == 200
        assert response.data == b'0'

    def test_complete_order(self):
        response = app.test_client().get('/complete-order')

        assert response.status_code == 200
        assert response.data == b'Order completed'

    def test_create_cart(self):
        cart = ShoppingCart(1)
        assert cart.order_number == 1
        assert cart.pizzas == []
        assert cart.drinks == {}
        assert cart.total == 0.0
        assert cart.valid_drinks == [
            "water", "coke", "nestea", "mountain dew", "canada dry"]

    @patch('builtins.input')
    def test_add_drink(self, input):
        set_cart(1)
        cart = get_client_cart()
        input.side_effect = ['water', '1']
        client_add_drinks()
        assert cart.drinks == {"water": 1}

    @patch('builtins.input')
    def test_add_invalid_drink(self, input):
        set_cart(1)
        cart = get_client_cart()
        input.side_effect = ['pepsi', '1']
        client_add_drinks()
        assert cart.drinks == {}

    @patch('builtins.input')
    def test_remove_drink(self, input):
        set_cart(1)
        cart = get_client_cart()
        input.side_effect = ['water', '1', 'water', '1']
        client_add_drinks()
        client_remove_drinks()
        assert cart.drinks == {"water": 0}

    @patch('builtins.input')
    def test_remove_invalid_drink(self, input):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        input.side_effect = ['water', '1', 'pepsi', '1']
        client_add_drinks()
        result_string = client_remove_drinks()
        assert cart.drinks == {"water": 1}
        assert result_string == "Invalid drink. Try again."

    @patch('builtins.input')
    def test_remove_invalid_quantity_of_drinks(self,input):
        set_cart(1)
        cart = get_client_cart()
        input.side_effect = ['water', '1', 'water', '500']
        client_add_drinks()
        return_value = client_remove_drinks()
        assert cart.drinks == {"water": 1}
        assert return_value == "You are removing more drinks than you have. Try again."

    @patch('builtins.input', return_value="1")
    def test_add_pizza_to_cart(self, input):
        expected_pizza = Pizza(1, 0)
        expected_pizza.size = "Small"
        cart = get_client_cart()
        accept_input(input.return_value)
        assert cart.pizzas[0].id == expected_pizza.id
        assert cart.pizzas[0].size == expected_pizza.size

    @patch('builtins.input', return_value=0)
    def test_remove_pizza_from_cart(self, input):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        add_pizza_to_cart(Pizza(1, 0))
        input.side_effect = ['0']
        accept_input("2")
        assert cart.pizzas == []

    @patch('builtins.input')
    def test_invalid_remove_pizza_from_cart(self, input):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        add_pizza_to_cart(Pizza(1, 0))
        old_pizza_array = cart.pizzas.copy()
        input.side_effect = ['1']
        accept_input("2")
        assert cart.pizzas == old_pizza_array

    @patch('builtins.input')
    def test_view_cart(self, input):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        input.side_effect = ['water', '1']
        accept_input("4")
        self.assertEqual(client_view_cart(), cart.view_cart())

    def test_clear_cart(self):
        cart = get_client_cart()
        client_clear_cart()
        assert cart.pizzas == []
        assert cart.drinks == {}
        assert cart.total == 0.0

    @patch('builtins.input')
    def test_update_cart_price(self, input):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        custom_pizza = Pizza(3, 2)
        custom_pizza.size = "Small"
        custom_pizza.calculate_price()
        cart.add_pizza(custom_pizza)
        input.side_effect = ['2', '2', '3', '0', '0']
        accept_input("3")
        custom_pizza.calculate_price()
        assert cart.total == 12

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

    def test_change_dough_on_pizza_white(self):
        pizza = Pizza(1, 1)
        pizza.choose_dough(1)
        self.assertEqual(pizza.dough, "White")

    def test_choose_dough_on_new_custom_pizza(self):
        pizza = Pizza(4, 1)
        pizza.choose_dough(3)
        self.assertEqual(pizza.dough, "Cauliflower")

        # choose_size TESTS

    def test_change_pizza_size(self):
        pizza = Pizza(1, 1)
        pizza.choose_size(1)
        self.assertEqual(pizza.size, "Small")

    def test_change_pizza_size_large(self):
        pizza = Pizza(1, 1)
        pizza.choose_size(3)
        self.assertEqual(pizza.size, "Large")

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

    def test_price_calculated_default_pizza(self):
        pizza = Pizza(3, 1)
        pizza.choose_size(2)
        pizza.choose_dough(2)
        pizza.calculate_price()
        self.assertEqual(pizza.price, 13.5)

    def test_price_calculated_default_pizza_large(self):
        pizza = Pizza(3, 1)
        pizza.choose_size(3)
        pizza.choose_dough(2)
        pizza.calculate_price()
        self.assertEqual(pizza.price, 15.5)

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

        # change_price TEST
    def test_price_calculated_custom_pizza(self):
        pizza = Pizza(4, 5)
        pizza.choose_dough(3)
        pizza.choose_size(4)
        for i in range(1, 7):
            pizza.add_topping(i)
        pizza.calculate_price()
        pizza.change_price(50)
        self.assertEqual(pizza.price, 50)

        #CSV and JSON generation test

    def test_csv_generated_properly(self):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        pizza = Pizza(1,0)
        pizza.choose_size(1)
        pizza.calculate_price()
        cart.add_pizza(pizza)
        csv_string = csv_generation("123 abc lane", 99)
        expected_string = 'Order address:, Order Details for Pizza, Order Details for Price,\
        Order Details for Drinks, Order Number\n'
        expected_string += '123 abc lane, Small: {1: \'pepperoni\'}, $9.00, {} ($1.50 each), 99\n'
        assert csv_string == expected_string

    def test_csv_generated_properly_only_drinks(self):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        cart.add_drink("water", 2)
        csv_string = csv_generation("123 abc lane", 99)
        expected_string = 'Order address:, Order Details for Pizza, Order Details for Price,\
        Order Details for Drinks, Order Number\n'
        expected_string += '123 abc lane, No Pizzas , No Pizza Prices, {\'water\': 2} ($1.50 each), 99\n'
        assert csv_string == expected_string

    def test_csv_generated_properly_no_pizzas_or_drinks(self):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        csv_string = csv_generation("123 abc lane", 99)
        expected_string = 'Order address:, Order Details for Pizza, Order Details for Price,\
        Order Details for Drinks, Order Number\n'
        assert csv_string == expected_string

    def test_json_generated_properly(self):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        pizza = Pizza(1,0)
        pizza.choose_size(1)
        pizza.calculate_price()
        cart.add_pizza(pizza)
        json_dict = json_generation("123 abc lane", 99)
        assert json_dict["Order address"] == "123 abc lane"
        assert json_dict["Order number"] == "99"
        assert json_dict["Order details"] == "Small: {1: \'pepperoni\'}, $9.00, {} ($1.50 each), \n"

    def test_json_generated_properly_no_pizzas_or_drinks(self):
        set_cart(99)
        cart = get_client_cart()
        client_clear_cart()
        cart.add_drink("water", 5)
        json_dict = json_generation("123 abc lane", 99)
        assert json_dict["Order address"] == "123 abc lane"
        assert json_dict["Order number"] == "99"
        assert json_dict["Order details"] == "No Pizzas , No Pizza Prices, {'water': 5} ($1.50 each)"
