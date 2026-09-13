from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Warehouse, Product, Stock

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class StockOperationSerializer(serializers.Serializer):
    warehouse_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        user = self.context['request'].user
        action_type = self.context.get('action_type')

        warehouse_id = data.get('warehouse_id')
        product_id = data.get('product_id')
        req_quantity = data.get('quantity')

        try:
            warehouse = Warehouse.objects.get(id=warehouse_id)
        except Warehouse.DoesNotExist:
            raise serializers.ValidationError("Склад не найден.")

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Товар не найден.")

        if action_type == 'supply' and user.user_type != User.UserType.SUPPLIER:
            raise serializers.ValidationError(
                "Только поставщики могут поставлять товары."
            )

        if action_type == 'consume' and user.user_type != User.UserType.CONSUMER:
            raise serializers.ValidationError(
                "Только потребители могут получать товары."
            )

        if action_type == 'consume':
            stock = Stock.objects.filter(
                warehouse=warehouse,
                product=product
            ).first()

            if not stock or stock.quantity < req_quantity:
                raise serializers.ValidationError(
                    f"Недостаточно товара на складе! "
                    f"Доступное количество: {stock.quantity if stock else 0}"
                )

        data['warehouse'] = warehouse
        data['product'] = product
        return data