# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Product Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_models.py:TestProductModel

"""
import os
import logging
import unittest
from decimal import Decimal
from service.models import Product, Category, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = ProductFactory()
        logging.info('Random Product created: Test Case: test create a product')
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        
        #fetching the id from Product
        found_product = Product.find(product.id)
        # product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        # self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertTrue(found_product is not None)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.description, product.description)
        self.assertEqual(found_product.available, product.available)
        self.assertEqual(found_product.price, product.price)
        self.assertEqual(found_product.category, product.category)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = ProductFactory()
        product.id = None
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)
        # Check that it matches the original product
        new_product = products[0]
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(new_product.description, product.description)
        self.assertEqual(Decimal(new_product.price), product.price)
        self.assertEqual(new_product.available, product.available)
        self.assertEqual(new_product.category, product.category)

    #
    # ADD YOUR TEST CASES HERE
    #

    def test_read_a_product(self):
        """It should read a product"""
        product = ProductFactory()
        product.id = None
        product.create()
        logging.info(f'Random Product created: {product.id}')
        self.assertIsNotNone(product.id)
        
        #fetching/reading the product from Product
        found_product = Product.find(product.id)
        logging.info(f'Fetching product: {product.id}')
        
        # Assertions
        # self.assertTrue(found_product is not None)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.description, product.description)
        self.assertEqual(found_product.available, product.available)
        self.assertEqual(found_product.price, product.price)
        self.assertEqual(found_product.category, product.category)
    
    def test_update_a_product(self):
        """It should update a product"""
        product = ProductFactory()
        product.id = None
        product.create()
        logging.info(f'Random Product created: {product.id} | description = {product.description}')
        self.assertIsNotNone(product.id)
        
        #updating the description field
        original_id = product.id
        product.description = 'something!'
        product.update()
        # making sure that the item was updated correctly
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.description, 'something!')
        
        #fetching/reading the product(s) from Product
        all_products = Product.all()
        logging.info(f'Fetching product: {product.id} | description = {product.description}')
        
        # Assertions after update and fetch operations
        self.assertEqual(len(all_products),1) # assert only one product is present
        self.assertTrue(all_products[0].id, original_id)
        self.assertEqual(all_products[0].description, 'something!')
        
    def test_delete_a_product(self):
        """It should delete a product"""
        product = ProductFactory()
        product.create()
        logging.info(f'Random Product created: {product.id}')
        self.assertIsNotNone(product.id)
 
        all_products = Product.all()
        self.assertEqual(len(all_products),1) # assert only one product is present
        
        #deleting the product
        product.delete()
        all_products = Product.all()
        self.assertEqual(len(all_products),0) # assert no product is present

    def test_list_all_products(self):
        """It should list all product"""
        all_products = Product.all()
        self.assertEqual(all_products,[]) # assert the list is empty
        
        # creating few products
        for elem in range(5):
            product = ProductFactory()
            product.create()
            logging.info(f'Random Product created: {product.id}')
        
        # listing all products
        all_products = Product.all()
        self.assertEqual(len(all_products),5)

    def test_find_product_by_name(self):
        """It should find product by name"""
        products = ProductFactory.create_batch(5)
        
        for product in products:
            product.create()
        
        first_name = products[0].name
        count  = len([product for product in products if product.name == first_name])
        found_products = Product.find_by_name(first_name)
        
        # Assertions
        self.assertEqual(found_products.count(),count)
        for product in found_products:
            self.assertEqual(product.name, first_name)

    def test_find_product_by_availability(self):
        """It should find product by availability"""
        products = ProductFactory.create_batch(10)
        
        for product in products:
            product.create()
        
        first_availability = products[0].available
        count = len([product for product in products if product.available == first_availability])
        found_products = Product.find_by_availability(first_availability)
        
        # Assertions
        self.assertEqual(found_products.count(),count)
        for product in found_products:
            self.assertEqual(product.available, first_availability)

    def test_find_product_by_category(self):
        """It should find product by category"""
        products = ProductFactory.create_batch(10)
        
        for product in products:
            product.create()
        
        first_category = products[0].category
        count = len([product for product in products if product.category == first_category])
        found_products = Product.find_by_category(first_category)
        
        # Assertions
        self.assertEqual(found_products.count(),count)
        for product in found_products:
            self.assertEqual(product.category, first_category)