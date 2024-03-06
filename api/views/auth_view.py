from django.http import JsonResponse
from django.db import connection
# from ..models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

import jwt
from datetime import datetime, timedelta

SECRET_KEY = 'thesungoesdownthestarscomeoutandallthatcountsishereandnow'


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    data = request.data
    email = data.get("email")
    password = data.get("password")

    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT * FROM "User" WHERE email = %s AND password = %s',
            [email, password]
        )
        user_data = cursor.fetchone()
        print(user_data)

    if not user_data:
        return Response(
            {"error": "Invalid email or password"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user_id = user_data[0]
    first_name = user_data[1]
    last_name = user_data[2]
    username = user_data[3]
    user_email = user_data[4]

    expiration_time = datetime.utcnow() + timedelta(days=7)

    payload = {
        "user_id": user_id,
        "email": user_email,
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "exp": expiration_time
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return Response({
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": expiration_time
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data = request.data
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")

    if not email or not password or not first_name or not last_name:
        return Response(
            {"error": "Please provide all fields"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    username = f"{first_name.lower()}.{last_name.lower()}"
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT * FROM "User" WHERE username = %s', [username])
        existing_user = cursor.fetchone()

    # TODO: fix duplicate username
    suffix = 1
    while existing_user:
        username = f"{first_name.lower()}.{last_name.lower()}{suffix}"
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM "User" WHERE username = %s', [username])
            existing_user = cursor.fetchone()
        suffix += 1

    if len(password) < 8:
        return Response(
            {"error": "Password must be at least 8 characters"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO "User" (username, first_name, last_name, email, password) VALUES (%s, %s, %s, %s, %s)',
                [username, first_name, last_name, email, password]
            )

    except Exception as e:
        return Response(
            {"error": "Failed to create user"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response({
        "message": "User created successfully"
    }, status=status.HTTP_201_CREATED)
