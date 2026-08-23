from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class UserType(models.TextChoices):
        SUPPLIER = 'supplier', 'Поставщик'
        CONSUMER = 'consumer', 'Потребитель'

    user_type = models.CharField(
        max_length=20,  # max_choices əvəzinə max_length yazılır
        choices=UserType.choices,
        default=UserType.CONSUMER
    )
    email = models.EmailField(unique=True)


class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Stock(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stocks')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks')
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.warehouse.name}: {self.quantity}"