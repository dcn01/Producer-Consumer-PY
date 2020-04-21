"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
from time import sleep


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):

        #Constructor.

        #Thread constructor
        Thread.__init__(self, **kwargs)

        #@type products: List()
        #@param products: a list of products that the producer will produce
        self.products = products

        #@type marketplace: Marketplace
        #@param marketplace: a reference to the marketplace
        self.marketplace = marketplace

        #:type producer_id: Int
        #:param producer_id: unique identifier for consumers
        self.producer_id = marketplace.register_producer()

        #@type republish_wait_time: Time
        #@param republish_wait_time: the number of seconds that a producer must
        #wait until the marketplace becomes available
        self.republish_wait_time = republish_wait_time

        #@type kwargs:
        #@param kwargs: other arguments that are passed to the Thread's __init__()
        self.kwargs = kwargs


    def run(self):
        index = 0
        length = len(self.products)
        while True:
            for i in range(self.products[index][1]):
                if not self.marketplace.publish(self.producer_id, self.products[index][0]):
                    sleep(self.republish_wait_time)
                    i -= 1
                else:
                    sleep(self.products[index][2])
            index = (index + 1) % length
