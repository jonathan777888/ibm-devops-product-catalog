import unittest
from service.routes import app
from service.models import db, Product, Category, DataValidationError
from tests.factories import ProductFactory


class TestProductModel(unittest.TestCase):
    """Test cases for the Product model."""

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_a_product(self):
        """It should create a product."""
        product = ProductFactory()
        product.create()
        self.assertIsNotNone(product.id)

    def test_read_a_product(self):
        """It should read a product."""
        product = ProductFactory()
        product.create()
        found_product = Product.find(product.id)
        self.assertIsNotNone(found_product)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)

    def test_update_a_product(self):
        """It should update a product."""
        product = ProductFactory()
        product.create()
        product.name = "Updated Product"
        product.update()
        updated_product = Product.find(product.id)
        self.assertEqual(updated_product.name, "Updated Product")

    def test_delete_a_product(self):
        """It should delete a product."""
        product = ProductFactory()
        product.create()
        product_id = product.id
        product.delete()
        deleted_product = Product.find(product_id)
        self.assertIsNone(deleted_product)

    def test_list_all_products(self):
        """It should list all products."""
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        all_products = Product.all()
        self.assertEqual(len(all_products), 5)

    def test_find_by_name(self):
        """It should find products by name."""
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        target_product = products[0]
        found_products = Product.find_by_name(target_product.name).all()
        self.assertGreaterEqual(len(found_products), 1)
        self.assertEqual(found_products[0].name, target_product.name)

    def test_find_by_category(self):
        """It should find products by category."""
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        target_product = products[0]
        found_products = Product.find_by_category(target_product.category).all()
        self.assertGreaterEqual(len(found_products), 1)
        self.assertEqual(found_products[0].category, target_product.category)

    def test_find_by_availability(self):
        """It should find products by availability."""
        available_product = ProductFactory(available=True)
        unavailable_product = ProductFactory(available=False)
        available_product.create()
        unavailable_product.create()
        found_products = Product.find_by_availability(True).all()
        self.assertGreaterEqual(len(found_products), 1)
        for product in found_products:
            self.assertTrue(product.available)

    def test_serialize_a_product(self):
        """It should serialize a product."""
        product = ProductFactory()
        data = product.serialize()
        self.assertEqual(data["name"], product.name)
        self.assertEqual(data["description"], product.description)
        self.assertEqual(data["price"], product.price)
        self.assertEqual(data["available"], product.available)
        self.assertEqual(data["category"], product.category.name)

    def test_deserialize_a_product(self):
        """It should deserialize a product."""
        data = {
            "name": "Product Name",
            "description": "Product description",
            "price": 10.99,
            "available": True,
            "category": "FOOD",
        }
        product = Product()
        product.deserialize(data)
        self.assertEqual(product.name, "Product Name")
        self.assertEqual(product.description, "Product description")
        self.assertEqual(product.price, 10.99)
        self.assertTrue(product.available)
        self.assertEqual(product.category, Category.FOOD)

    def test_deserialize_missing_data(self):
        """It should not deserialize a product with missing data."""
        data = {
            "name": "Product Name",
            "description": "Product description",
            "price": 10.99,
        }
        product = Product()
        with self.assertRaises(DataValidationError):
            product.deserialize(data)


if __name__ == "__main__":
    unittest.main()
