import unittest
from service.routes import app
from service.models import db, Category
from tests.factories import ProductFactory


BASE_URL = "/products"


class TestProductRoutes(unittest.TestCase):
    """Test cases for Product REST API routes."""

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    def setUp(self):
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def _create_products(self, count):
        """Create products directly in the test database."""
        products = ProductFactory.create_batch(count)
        for product in products:
            product.create()
        return products

    def test_create_a_product(self):
        """It should create a product."""
        product = ProductFactory()
        payload = product.serialize()
        response = self.client.post(BASE_URL, json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["name"], product.name)
        self.assertIn("Location", response.headers)

    def test_read_a_product(self):
        """It should read a product."""
        product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}/{product.id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["id"], product.id)
        self.assertEqual(data["name"], product.name)

    def test_update_a_product(self):
        """It should update a product."""
        product = self._create_products(1)[0]
        payload = product.serialize()
        payload["name"] = "Updated Product"
        payload["description"] = "Updated description"
        response = self.client.put(f"{BASE_URL}/{product.id}", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["id"], product.id)
        self.assertEqual(data["name"], "Updated Product")
        self.assertEqual(data["description"], "Updated description")

    def test_delete_a_product(self):
        """It should delete a product."""
        product = self._create_products(1)[0]
        response = self.client.delete(f"{BASE_URL}/{product.id}")
        self.assertEqual(response.status_code, 204)
        response = self.client.get(f"{BASE_URL}/{product.id}")
        self.assertEqual(response.status_code, 404)

    def test_list_all_products(self):
        """It should list all products."""
        self._create_products(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_query_by_name(self):
        """It should list products by name."""
        products = self._create_products(5)
        target_product = products[0]
        response = self.client.get(BASE_URL, query_string={"name": target_product.name})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]["name"], target_product.name)

    def test_query_by_category(self):
        """It should list products by category."""
        product_1 = ProductFactory(category=Category.FOOD)
        product_2 = ProductFactory(category=Category.CLOTHS)
        product_1.create()
        product_2.create()
        response = self.client.get(BASE_URL, query_string={"category": "FOOD"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreaterEqual(len(data), 1)
        for product in data:
            self.assertEqual(product["category"], "FOOD")

    def test_query_by_availability(self):
        """It should list products by availability."""
        product_1 = ProductFactory(available=True)
        product_2 = ProductFactory(available=False)
        product_1.create()
        product_2.create()
        response = self.client.get(BASE_URL, query_string={"available": "true"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreaterEqual(len(data), 1)
        for product in data:
            self.assertTrue(product["available"])


if __name__ == "__main__":
    unittest.main()
