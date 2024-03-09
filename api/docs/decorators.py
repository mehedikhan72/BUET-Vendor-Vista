from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import serializers


class UserRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)


def user_register_swagger_schema():
    return swagger_auto_schema(
        method='post',
        request_body=UserRegistrationSerializer,
        responses={200: 'Success', 400: 'Bad Request'},
        operation_summary='User Registration',
        operation_description='Register a new user.',
        security=[],
        tags=['Authentication'],
    )


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)


def user_login_swagger_schema():
    return swagger_auto_schema(
        method='post',
        request_body=UserLoginSerializer,
        responses={200: 'Success', 400: 'Bad Request'},
        operation_summary='User Login',
        operation_description='Login a user.',
        security=[],
        tags=['Authentication'],
    )


class AddProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=100)
    price = serializers.FloatField()
    quantity = serializers.IntegerField()
    category = serializers.CharField(max_length=100)
    multiple_products = serializers.BooleanField()
    used = serializers.BooleanField()


def add_product_swagger_schema():
    return swagger_auto_schema(
        method='post',
        request_body=AddProductSerializer,
        responses={200: 'Success', 400: 'Bad Request'},
        operation_summary='Add Product',
        operation_description='Add a new product.',
        security=[
            {
                'Bearer': []
            }
        ],
        tags=['Product'],
    )
