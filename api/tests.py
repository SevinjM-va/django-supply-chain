from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from api.models import Warehouse, Product, Stock


User = get_user_model()


class WarehouseAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.supplier = User.objects.create_user(
            username='supplier_test',
            email='supplier@test.com',
            password='Test12345!'
        )
        self.supplier.user_type = User.UserType.SUPPLIER
        self.supplier.save()

        self.consumer = User.objects.create_user(
            username='consumer_test',
            email='consumer@test.com',
            password='Test12345!'
        )
        self.consumer.user_type = User.UserType.CONSUMER
        self.consumer.save()

        self.warehouse = Warehouse.objects.create(
            name='Test Warehouse',
            location='Ganja'
        )

        self.product = Product.objects.create(
            name='Test Laptop',
            description='Test product'
        )

    def get_token(self, username, password='Test12345!'):
        response = self.client.post(
            '/api/login/',
            {
                'username': username,
                'password': password
            }
        )
        return response.data['access']

    def test_supplier_can_supply_product(self):
        token = self.get_token('supplier_test')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )

        response = self.client.post(
            '/api/stocks/supply/',
            {
                'warehouse_id': self.warehouse.id,
                'product_id': self.product.id,
                'quantity': 10
            },
            format='json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['current_stock'], 10)

    def test_consumer_can_consume_product(self):
        Stock.objects.create(
            warehouse=self.warehouse,
            product=self.product,
            quantity=10
        )

        token = self.get_token('consumer_test')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )

        response = self.client.post(
            '/api/stocks/consume/',
            {
                'warehouse_id': self.warehouse.id,
                'product_id': self.product.id,
                'quantity': 3
            },
            format='json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['current_stock'], 7)

    def test_consumer_cannot_consume_more_than_stock(self):
        Stock.objects.create(
            warehouse=self.warehouse,
            product=self.product,
            quantity=5
        )

        token = self.get_token('consumer_test')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )

        response = self.client.post(
            '/api/stocks/consume/',
            {
                'warehouse_id': self.warehouse.id,
                'product_id': self.product.id,
                'quantity': 10
            },
            format='json'
        )

        self.assertEqual(response.status_code, 400)

    def test_consumer_cannot_supply(self):
        token = self.get_token('consumer_test')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )

        response = self.client.post(
            '/api/stocks/supply/',
            {
                'warehouse_id': self.warehouse.id,
                'product_id': self.product.id,
                'quantity': 10
            },
            format='json'
        )

        self.assertEqual(response.status_code, 400)