from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from .models import Warehouse, Product, Stock
from .serializers import (
    UserRegistrationSerializer, 
    WarehouseSerializer, 
    ProductSerializer, 
    StockOperationSerializer
)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class StockViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def supply(self, request):
        serializer = StockOperationSerializer(
            data=request.data,
            context={'request': request, 'action_type': 'supply'}
        )

        if serializer.is_valid():
            warehouse = serializer.validated_data['warehouse']
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']

            stock, created = Stock.objects.get_or_create(
                warehouse=warehouse,
                product=product
            )
            stock.quantity += quantity
            stock.save()

            return Response(
                {
                    "message": "The product was successfully added to the warehouse.",
                    "current_stock": stock.quantity
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['post'])
    def consume(self, request):

        serializer = StockOperationSerializer(
            data=request.data,
            context={'request': request, 'action_type': 'consume'}
        )

        if serializer.is_valid():
            warehouse = serializer.validated_data['warehouse']
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']

            stock = Stock.objects.get(
                warehouse=warehouse,
                product=product
            )
            stock.quantity -= quantity
            stock.save()

            return Response(
                {
                    "message": "The product was successfully removed from the warehouse.",
                    "current_stock": stock.quantity
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )