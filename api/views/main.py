from ..docs.decorators import add_product_swagger_schema
import os
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import TemporaryUploadedFile
import json
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

# INFO: In case for a product not having a color or size, the user will have to add a color or size with the quantity of the product, from the frontend.

# @add_product_swagger_schema()


@csrf_exempt
# @api_view(['POST'])
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


@csrf_exempt
@permission_classes([AllowAny])
def add_product_color(request, id):
    if request.method == "POST":
        user_id = get_user(request.headers.get("Authorization").split(" ")[1])

        if user_id == "expired" or user_id == "invalid":
            return JsonResponse({"error": "Invalid token"}, status=401)

        product_owner_id = None
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT owner_id FROM "Product" WHERE id = %s',
                [id]
            )
            product_owner_id = cursor.fetchone()

        product_owner_id = product_owner_id[0]
        if product_owner_id != user_id:
            return JsonResponse({"error": "You are not the owner of this product"}, status=401)

        color = request.POST.get("color")
        quantity = request.POST.get("quantity")
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO "ProductColor" (color, product_id, quantity) VALUES (%s, %s, %s)',
                [color, id, quantity]
            )

        return JsonResponse({"message": "Color added successfully"}, status=201)

    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
@permission_classes([AllowAny])
def add_product_image(request, id):
    if request.method == "POST":
        user_id = get_user(request.headers.get("Authorization").split(" ")[1])

        if user_id == "expired" or user_id == "invalid":
            return JsonResponse({"error": "Invalid token"}, status=401)

        product_owner_id = None
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT owner_id FROM "Product" WHERE id = %s',
                [id]
            )
            product_owner_id = cursor.fetchone()

        product_owner_id = product_owner_id[0]
        if product_owner_id != user_id:
            return JsonResponse({"error": "You are not the owner of this product"}, status=401)

        images = request.FILES.getlist("images")
        for image in images:
            print("IMAGEEEEE")

            # store image in the media root
            default_storage.save(image.name, image)
            image = str(image)
            print(image)

            with connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO "ProductImage" (url, product_id) VALUES (%s, %s)',
                    [image, id]
                )

        return JsonResponse({"message": "Images added successfully"}, status=201)

    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
@permission_classes([AllowAny])
def add_product_size(request, id):
    if request.method == "POST":
        user_id = get_user(request.headers.get("Authorization").split(" ")[1])

        if user_id == "expired" or user_id == "invalid":
            return JsonResponse({"error": "Invalid token"}, status=401)

        product_owner_id = None
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT owner_id FROM "Product" WHERE id = %s',
                [id]
            )
            product_owner_id = cursor.fetchone()

        product_owner_id = product_owner_id[0]
        if product_owner_id != user_id:
            return JsonResponse({"error": "You are not the owner of this product"}, status=401)

        size = request.POST.get("size")
        quantity = request.POST.get("quantity")
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO "ProductSize" (size, product_id, quantity) VALUES (%s, %s, %s)',
                [size, id, quantity]
            )

        return JsonResponse({"message": "Size added successfully"}, status=201)

    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
@permission_classes([AllowAny])
def place_order(request):
    if request.method == "POST":
        user_id = get_user(request.headers.get("Authorization").split(" ")[1])

        if user_id == "expired" or user_id == "invalid":
            return JsonResponse({"error": "Invalid token"}, status=401)

        data = json.loads(request.body)
        print(data)

        status = "pending"
        order_date = datetime.now()
        # for now, will be updated later, based on the items ordered.
        total_price = 0
        payment_method = "COD"
        shipping_address = data["shipping_address"]
        delivery_date = datetime.now() + timedelta(days=7)
        trnx_id = "null"

        ordered_items = data["ordered_items"]

        at_least_one_item_ordered = False
        items_skipped = 0

        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO "Order" (status, order_date, total_price, payment_method, shipping_address, delivery_date, trnx_id, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                [status, order_date, total_price, payment_method,
                    shipping_address, delivery_date, trnx_id, user_id]
            )

            cursor.execute(
                'SELECT id FROM "Order" WHERE user_id = %s ORDER BY id DESC LIMIT 1',
                [user_id]
            )
            order_id = cursor.fetchone()

            for item in ordered_items:
                product_id = item["product_id"]
                quantity = item["quantity"]
                size = item["size"]
                color = item["color"]
                price = None

                cursor.execute(
                    'SELECT price FROM "Product" WHERE id = %s',
                    [product_id]
                )
                price = cursor.fetchone()[0]

                # checks availability thru sql functions.
                # if unavailable, skip that item and return a message to the user.

                cursor.execute(
                    "SELECT validate_product_color(%s, %s, %s)",
                    [product_id, color, quantity]
                )

                quantity_ok_for_color = cursor.fetchone()[0]
                cursor.execute(
                    "SELECT validate_product_size(%s, %s, %s)",
                    [product_id, size, quantity]
                )
                quantity_ok_for_size = cursor.fetchone()[0]

                if quantity_ok_for_color == 'no' or quantity_ok_for_size == 'no':
                    items_skipped += 1
                    continue

                cursor.execute(
                    'INSERT INTO "OrderedItem" (quantity, size, color, price, order_id, product_id) VALUES (%s, %s, %s, %s, %s, %s)',
                    [quantity, size, color, price, order_id, product_id]
                )
                at_least_one_item_ordered = True

                # Trigger works here! updates product quantity.
            if at_least_one_item_ordered:
                # update order's total price
                cursor.execute(
                    'CALL update_order_total_price_proc(%s)',
                    [order_id]
                )

                if items_skipped == 0:
                    return JsonResponse({"message": "Order placed successfully"}, status=201)
                else:
                    return JsonResponse({"message": "Order placed successfully, but {items_skipped} items of your order are not available. Try with a lesser quantity"}, status=201)

            else:
                # we need to delete that order since no items were ordered.
                cursor.execute(
                    'DELETE FROM "Order" WHERE id = %s',
                    [order_id]
                )

                return JsonResponse({"error": "No items were ordered. Try with a lesser quantity"}, status=400)


def get_products(request, category):
    if request.method == "GET":
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM "Product" WHERE category = %s',
                [category]
            )
            products = cursor.fetchall()

        return JsonResponse({"products": products}, status=200)


@csrf_exempt
@permission_classes([AllowAny])
def update_product_quantity(request, id):
    # updates product's quantity for each color and size

    if request.method == "POST":
        user_id = get_user(request.headers.get("Authorization").split(" ")[1])

        if user_id == "expired" or user_id == "invalid":
            return JsonResponse({"error": "Invalid token"}, status=401)

        product_owner_id = None
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT owner_id FROM "Product" WHERE id = %s',
                [id]
            )
            product_owner_id = cursor.fetchone()

        product_owner_id = product_owner_id[0]
        if product_owner_id != user_id:
            return JsonResponse({"error": "You are not the owner of this product"}, status=401)

        size = request.POST.get("size")
        color = request.POST.get("color")
        quantity = request.POST.get("quantity")

        if size:
            # INFO: a trigger will update the quantity of the product, the trigger will run for each color entry,
            # given that the ui must prompt the user to add both color and a size while updating quantity
            with connection.cursor() as cursor:
                cursor.execute(
                    'UPDATE "ProductSize" SET quantity = %s WHERE product_id = %s AND size = %s',
                    [quantity, id, size]
                )

        if color:
            with connection.cursor() as cursor:
                cursor.execute(
                    'UPDATE "ProductColor" SET quantity = %s WHERE product_id = %s AND color = %s',
                    [quantity, id, color]
                )

        return JsonResponse({"message": "Product quantity updated successfully"}, status=200)

    else:
        return JsonResponse({"error": "Invalid request, only put methods are allowed."}, status=400)


@csrf_exempt
@permission_classes([AllowAny])
def add_review(request, id):
    if request.method == "POST":
        user_id = get_user(request.headers.get("Authorization").split(" ")[1])

        if user_id == "expired" or user_id == "invalid":
            return JsonResponse({"error": "Invalid token"}, status=401)

        product_owner_id = None
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT owner_id FROM "Product" WHERE id = %s',
                [id]
            )
            product_owner_id = cursor.fetchone()

        product_owner_id = product_owner_id[0]
        if product_owner_id == user_id:
            print(product_owner_id)
            print(user_id)
            return JsonResponse({"error": "You are the owner of this product. You cannot add a review."}, status=401)

        review = request.POST.get("review")
        rating = request.POST.get("rating")
        review_exists = None  # for this user for this product

        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM "Review" WHERE user_id = %s AND product_id = %s',
                [user_id, id]
            )
            review_exists = cursor.fetchone()
            print(review_exists)

            if review_exists:
                return JsonResponse({"error": "You have already reviewed this product"}, status=400)

            cursor.execute(
                'CALL add_review_proc(%s, %s, %s, %s)',
                [user_id, id, review, rating]
            )

            cursor.execute(
                'SELECT * FROM "Review" WHERE user_id = %s AND product_id = %s',
                [user_id, id]
            )
            review_exists = cursor.fetchone()

            if review_exists:
                return JsonResponse({"message": "Review added successfully"}, status=201)

            else:
                return JsonResponse({"error": "Review not added. One possible reason could be you have not ordered this product yet."}, status=400)


@csrf_exempt
@permission_classes([AllowAny])
def ask_question(request, id):
    if request.method == "POST":
        user_id = get_user(request.headers.get("Authorization").split(" ")[1])

        if user_id == "expired" or user_id == "invalid":
            return JsonResponse({"error": "Invalid token"}, status=401)

        product_owner_id = None
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT owner_id FROM "Product" WHERE id = %s',
                [id]
            )
            product_owner_id = cursor.fetchone()

        product_owner_id = product_owner_id[0]
        if product_owner_id == user_id:
            return JsonResponse({"error": "You are the owner of this product. You cannot ask a question."}, status=401)

        question = request.POST.get("question")
        asked_date = datetime.now()

        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO "QnA" (question, asked_date, product_id, user_id) VALUES (%s, %s, %s, %s)',
                [question, asked_date, id, user_id]
            )

        return JsonResponse({"message": "Question asked successfully"}, status=201)


@csrf_exempt
@permission_classes([AllowAny])
def add_answer(request, id, qna_id):
    if request.method == "POST":
        user_id = get_user(request.headers.get("Authorization").split(" ")[1])

        if user_id == "expired" or user_id == "invalid":
            return JsonResponse({"error": "Invalid token"}, status=401)

        product_owner_id = None
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT owner_id FROM "Product" WHERE id = %s',
                [id]
            )
            product_owner_id = cursor.fetchone()

        product_owner_id = product_owner_id[0]
        answer = request.POST.get("answer")
        with connection.cursor() as cursor:
            cursor.execute(
                'CALL update_qna_answer_3(%s, %s, %s)',
                [qna_id, user_id, answer]
            )

            answer_added = None
            cursor.execute(
                'SELECT answer FROM "QnA" WHERE id = %s',
                [qna_id]
            )
            answer_added = cursor.fetchone()[0]
            print(answer_added)

            if answer_added:
                return JsonResponse({"message": "Answer added successfully"}, status=201)
            else:
                return JsonResponse({"error": "Answer not added."}, status=400)


@csrf_exempt
@permission_classes([AllowAny])
def add_report(request, id):
    user_id = get_user(request.headers.get("Authorization").split(" ")[1])
    description = request.POST.get("description")
    report_date = datetime.now()

    with connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO "Report" (description, report_date, user_id, product_id) VALUES (%s, %s, %s, %s)',
            [description, report_date, user_id, id]
        )

    return JsonResponse({"message": "Report added successfully"}, status=201)


@csrf_exempt
@permission_classes([AllowAny])
def get_top_selling_products(request):
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        limit = 10

        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM generate_top_selling_products_report3(%s, %s, %s)',
                [start_date, end_date, limit]
            )
            products = cursor.fetchall()

            return JsonResponse({"products": products}, status=200)
