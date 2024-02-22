from ..models import User, Product, ProductImage, ProductSize, ProductColor, Review, QnA, Report
from ..serializers import UserRegistrationSerializer, UserSerializer, ProductSerializer, ProductImageSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# import geenrics
from rest_framework import generics
from rest_framework import permissions

from django.db import connection


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        owner_id = self.request.user.id
        print(owner_id)

        sql_query = """
                    INSERT INTO api_product (id, name, description, price, available_quantity, status, multiple_products, used, category, owner, total_sold)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
        cursor = connection.cursor()
        cursor.execute(sql_query, (
            1,
            serializer.validated_data["name"],
            serializer.validated_data["description"],
            str(serializer.validated_data["price"]),
            str(serializer.validated_data["available_quantity"]),
            serializer.validated_data["status"],
            serializer.validated_data["multiple_products"],
            serializer.validated_data["used"],
            serializer.validated_data["category"],
            owner_id,
            0,
        ))
