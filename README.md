# Kanuli's Pizza
Welcome to the Kanuli's Pizza terminal. Here you have the ability to fill a cart with pizzas and drinks, along with the administrative ability to change the price of each pizza item and drinks in cart.

## Instructions
First, run the main flask module by running `python3 PizzaParlour.py`. Then run `python3 main.py` in a separate terminal to reach the main menu.

Here, you can enter several numerical inputs to proceed:
1. **Add Pizza to Cart:** Here, you will have the option to enter 1-3 to choose a size of one of the Kanuli Specials or enter 4 to create your own custom pizza: 
choosing dough type, toppings, and size.
2. **Remove Pizza from Cart:** This displays the pizzas currently in cart. Entering the associated pizza id will remove the pizza from the cart.
3. **Edit Pizza in Cart:** Displays the pizzas currently in cart. Entering the associated pizza id will give options to change dough, size, and add or remove toppings.
4. **Add Drink to Cart:** Given a list of drinks, type in the name of the drink and quantity you wish to add to cart.
5. **Remove Drink from Cart:** Type in the name of the drink and quantity you wish to remove from cart.
6. **View Cart:** Displays all the pizzas and drinks currently in cart, as well as each of their prices, cart subtotal and cart total.
7. **Cancel Order:** Clears Cart.
8. **View Menu:** Prints out the menu with suggested retail prices.
9. **Look up Menu Item:** If you enter a name of an item on the menu, a description of the item and its suggested price will be returned. 

* **98: Administrative Access - Edit Price of Pizza in Cart:** Displays the pizzas currently in cart. Entering the associated pizza id will give the option to edit its price.
* **99: Administrative Access - Edit Price of Drinks in Cart:** Choose the new price of drinks in cart.

* **10: Checkout:** If you're sure you want to checkout, enter your address and options for delivery will be given. Once delivery is chosen, terminal will terminate.
* **0:** Exits the terminal.

#### Unit Tests:
Run unit tests with coverage by running `pytest --cov-report term --cov=. tests/unit_tests.py`

## Program Design
  The design pattern used for this project was that of a Factory. Upon our initial meeting, we realized that each pizza may have different features but all need shared characteristics: toppings, dough, and size. In the same vein, orders may contain different items in a cart, but all need shared characteristics like pizzas in cart, drinks in cart, and subtotal. In using Factory method design, we are able create these two classes with a high level cohesion and utilize them in `PizzaParlour.py`.

  An order consists of making a ShoppingCart object and filling it with Pizza objects. Pizzas contain an id, a list of toppings, a size, a dough type, and their own price. ShoppingCarts contain an cart id, a list of pizzas, a list of drinks, and a subtotal made by accumulating all prices in it. As these two are only linked with functions to add Pizzas to ShoppingCart's pizza list, we are able to maintain low level of coupling between these two objects.

  Originally, the program was made with most of the object creation done server side. After creating a new branch, a lot of these functions were moved to the client side, which was then merged back to main.
  
  On completion of order, provided that the user selected a delivery service, a csv or JSON is sent to the server. In your server terminal, you will see the csv/JSON printed in the terminal. Of course, it does not show on the client terminal as that is a detail the user does not need to be made aware of.

#### Code Craftsmanship
PyCharm was used to keep a good programming/formatting style.

## Pair Programming Experience
### Process
  Before anything was written down, the first topic of discussion was program design. Over a zoom call, a shared document was made which listed what classes would need to be created, their order to be completed based on importance, and which tasks on this list we could designate to be pair programmed. The first on this list was a Pizza class.
  
  For the implementation of `Pizza.py`, JJ was the driver with Aaron was the navigator. This session entailed the creation of the class and the implementation of its initial main functions to: create a custom pizza, choose from premade pizzas, and edit a pizza by adding or removing toppings. 
  
  The following pair programming session had the roles reversed with the purpose now being the creation of `ShoppingCart.py`. This session would include the creation of the class and its initial main functions: adding and removing drinks to carts, adding and removing pizza objects to cart, and clearing cart. The foundation of `PizzaParlour.py` was also made during this time to utilize the Pizza and Cart objects with functions to place items in cart, but not enough that the program was yet functional.
  
  Some functions and slight changes were made to each of the two designated pair programmed files following these two initial sessions, but not big enough to warrant a screen-watching session.  Following substantial additions were sent as screenshots for approval before pushes, and small changes were just sent as messages to acknowledge.
  
  At a later date,  two final pair programming sessions were done in succession to include the sections now labelled Pizza Tests and Shopping Cart Tests in `unit_tests.py`. (Originally, pizza tests were in a file called test_pizza but was moved to unit_tests at a later date).
  
  The remainder of `PizzaParlour.py`, `main.py`, and `unit_tests.py` were worked on collaboratively but not pair programmed. Having already made a list of tasks in our initial meeting, the remainder of the tasks were split to be done by each person.
  
### Reflection
  The experience of pair programming was new to us both so having someone else watch while we wrote code started off a little strange. As we wrote more, it became clear that having a navigator made things a lot easier; little fixes involving syntax we may have forgot or ways to improve the efficiency of a statement were often topics of suggestion. It became easy to just keep working as a driver since the navigator has more of a step back from the tunnel vision that comes with coding for long periods and can keep track of what the next task would be.

  A downside to the experience were the hassles of finding an intersection between our availabilities. Finding time around our other responsibilities, the two initial paired sessions were done at night and before class respectively. It then became clear that with increasing work loads there wouldn't be too many opportunities to screen-watch each other, hence the subsequent edits being sent as screenshots for the other person to view at their own time, and the sessions for the respective unit tests were made to be as quick as possible. This wasn't all bad though: having been used to working by ourselves, the times we did find a shared couple of hours made it less of a work-at-your-own-pace experience and more one where we have to be as efficient as possible as we are not only working on our own time.
  
  In the end, it was a new experience for us both, and one we can learn and grow as developers from.
