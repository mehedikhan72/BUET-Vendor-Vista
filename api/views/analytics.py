from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from .main import get_user
from django.db import connection


@csrf_exempt
@permission_classes([AllowAny])
def get_total_sales_for_each_product(request, id):
    user_id = get_user(request.headers.get("Authorization").split(" ")[1])

    owner = None
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT owner_id FROM "Product" WHERE id = %s',
            [id]
        )
        owner = cursor.fetchone()[0]

    if owner != user_id:
        return JsonResponse(
            {
                "error": "You are not the owner of this product"
            },
            status=403
        )

    total_sales = 0
    total_sales_money = 0

    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT calculate_total_sales(%s, %s)',
            [user_id, id]
        )
        total_sales = cursor.fetchone()[0]

        cursor.execute(
            'SELECT calculate_total_price(%s, %s)',
            [user_id, id]
        )
        total_sales_money = cursor.fetchone()[0]

    return JsonResponse(
        {
            "total_sales": total_sales,
            "total_sales_money": total_sales_money
        },)


@csrf_exempt
@permission_classes([AllowAny])
def get_users_pending_orders(request):
    user_id = get_user(request.headers.get("Authorization").split(" ")[1])
    # get pending orders and relevant ordered items
    pending_orders = []

    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT * FROM "Order" WHERE user_id = %s AND status = %s',
            [user_id, "pending"]
        )
        pending_orders = cursor.fetchall()

    data = []

    for order in pending_orders:
        order_id = order[0]
        shipping_address = order[1]
        status = order[2]
        ordered_items = []

        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM "OrderedItem" WHERE order_id = %s',
                [order_id]
            )
            ordered_items = cursor.fetchall()

            data.append(
                {
                    "order_id": order_id,
                    "shipping_address": shipping_address,
                    "status": status,
                    "ordered_items": ordered_items
                }
            )

    return JsonResponse(data, safe=False)
