"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
from time import sleep


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):

        #Constructor.#

        #Thread constructor
        Thread.__init__(self, **kwargs)

        #:type carts: List
        #:param carts: a list of add and remove operationsz
        self.carts = carts

        #:type marketplace: Marketplace
        #:param marketplace: a reference to the marketplace
        self.marketplace = marketplace

        #:type consumer_name: Int
        #:param consumer_name: unique identifier for consumers
        self.consumer_name = kwargs['name']

        #:type retry_wait_time: Time
        #:param retry_wait_time: the number of seconds that a producer must wait
        #until the Marketplace becomes available
        self.retry_wait_time = retry_wait_time

        #:type kwargs:
        #:param kwargs: other arguments that are passed to the Thread's __init__()
        self.kwargs = kwargs


    def run(self):

        for orders in self.carts:
            cart = self.marketplace.new_cart()
            for order in orders:
                quantity = order['quantity']
                if order['type'] == 'add':
                    while quantity != 0:
                        if self.marketplace.add_to_cart(cart, order['product']):
                            quantity -= 1
                        else:
                            sleep(self.retry_wait_time)
                else:
                    while quantity != 0:
                        self.marketplace.remove_from_cart(cart, order['product'])
                        quantity -= 1
            products = self.marketplace.place_order(cart)
            for product in products:
                print(self.consumer_name + " bought " + str(product[0]))
