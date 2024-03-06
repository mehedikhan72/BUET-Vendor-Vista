from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# import geenrics
from rest_framework import generics
from rest_framework import permissions
from django.http import JsonResponse

import datetime
import jwt
from datetime import datetime, timedelta
from django.db import connection

from django.views.decorators.csrf import csrf_exempt


SECRET_KEY = 'thesungoesdownthestarscomeoutandallthatcountsishereandnow'

def get_user(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
        return user_id
    except jwt.ExpiredSignatureError:
        return "expired"
    except jwt.InvalidTokenError:
        return "invalid"
import json

@csrf_exempt
@permission_classes([AllowAny])
def add_product(request):
    if request.method == "POST":
        
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        date_posted = datetime.now()
        status = "active"
        category = request.POST.get("category")
        multiple_products = request.POST.get("multiple_products")
        used = request.POST.get("used")

        # get the user id.
        bearer_token = request.headers.get("Authorization")
        # get rid of the bearer part
        bearer_token = bearer_token.split(" ")[1]
        owner_id = get_user(bearer_token)

        if owner_id == "expired" or owner_id == "invalid":
            return JsonResponse({"error": "Invalid token"}, status=401)

        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO "Product" (name, description, price, quantity, date_posted, status, category, multiple_products, used, owner_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                [name, description, price, quantity, date_posted,
                    status, category, multiple_products, used, owner_id]
            )

        return JsonResponse({"message": "Product added successfully"}, status=201)

def get_products(request, category):
    if request.method == "GET":
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM "Product" WHERE category = %s',
                [category]
            )
            products = cursor.fetchall()

        return JsonResponse({"products": products}, status=200)