"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Semaphore

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        #Constructor

        #:type queue_size_per_producer: Int
        #:param queue_size_per_producer: the maximum size of a queue associated with each producer
        self.queue_size_per_producer = queue_size_per_producer

        #:type products: dict{Product : [Producer(as Int)]}
        #:for each product published keep the list of the producers
        self.products = {}

        #:type carts: dict{id(Int) : [Product, Producer]}
        #:in each cart save a pair formed by the product and who made that product
        self.carts = {}

        #:type: producers: dict{String : Int}
        #:maps a producer name to an index
        self.producers = {}

        #:type current_producer: Int
        #:param current_producer: current index for a new producer
        self.current_producer = 0

        #:type producer_sem: semaphore
        #:producer_sem: allows just one producer to register
        self.producer_sem = Semaphore(value=1)

        #:type current_cart: Int
        #:current_cart: current index for a new cart
        self.current_cart = 0

        #:type cart_sem: semaphore
        #:cart_sem: allows just one producer to register
        self.cart_sem = Semaphore(value=1)

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.producers[str(self.current_producer)] = 0
        new_producer = self.current_producer

        self.producer_sem.acquire()
        self.current_producer += 1
        self.producer_sem.release()

        return str(new_producer)

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        if self.producers[producer_id] == self.queue_size_per_producer:
            return False

        self.producers[producer_id] = self.producers[producer_id] + 1
        if not product in self.products:
            self.products[product] = []
        self.products[product].append(producer_id)
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer
        :returns an int representing the cart_id
        """
        self.carts[self.current_cart] = []
        new_cart = self.current_cart

        self.cart_sem.acquire()
        self.current_cart += 1
        self.cart_sem.release()

        return new_cart

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        if not product in self.products:
            return False

        if not cart_id in self.carts:
            self.carts[cart_id] = []

        if self.products[product]:
            producer = self.products[product][0]
            self.producers[producer] -= 1
            self.products[product].remove(producer)
            self.carts[cart_id].append([product, producer])
            return True

        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        cart = self.carts[cart_id]
        for pair in cart:
            if pair[0] == product:
                producer = pair[1]
                self.producers[producer] = self.producers[producer] + 1
                self.products[product].append(producer)
                cart.remove(pair)
                break

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        return self.carts[cart_id]
