from django.urls import path
from .views.auth_view import register, login
# from rest_framework_simplejwt.views import (
#     TokenRefreshView,
# )

from .views.main import (add_product, get_products, add_product_color, add_product_size,
                         add_product_image, place_order, update_product_quantity, add_review, ask_question,
                         add_answer, add_report, get_top_selling_products, cancel_order, delete_product, deliver_order,
                         search_products, get_top_rated_product_by_category, generate_top_selling_products_by_category)

from .views.analytics import (
    get_total_sales_for_each_product, get_users_pending_orders)

urlpatterns = [
    # auth
    # path("token/", MyTokenObtainPairView.as_view()),
    # path("token/refresh/", TokenRefreshView.as_view()),

    path("register/", register, name="register"),
    path("login/", login, name="login"),

    path("add-product/", add_product, name="add-product"),
    path("add-product-color/<int:id>/",
         add_product_color, name="add-product-color"),
    path("add-product-size/<int:id>/", add_product_size, name="add-product-size"),
    path("add-product-image/<int:id>/",
         add_product_image, name="add-product-image"),

    path('products/<str:category>/', get_products, name="get-products"),

    path('place-order/', place_order, name="place-order"),
    path('update-product-quantity/<int:id>/',
         update_product_quantity, name="update-product-quantity"),
    path('add-review/<int:id>/', add_review, name="add-review"),

    path('ask-question/<int:id>/', ask_question, name="ask-question"),
    path('add-answer/<int:id>/<int:qna_id>/', add_answer, name="add-answer"),
    path('get_total_sales/<int:id>/',
         get_total_sales_for_each_product, name="get_total_sales"),
    path('add-report/<int:id>/', add_report, name="add-report"),
    path('get-top-selling-products/', get_top_selling_products,
         name="get-top-selling-products"),
    path('cancel-order/<int:order_id>/', cancel_order, name='cancel-order'),
    path('delete-product/<int:id>/', delete_product, name='delete-product'),
    path('get-users-pending-orders/', get_users_pending_orders,
         name='get-users-pending-orders'),
    path('deliver-order/<int:order_id>/', deliver_order, name='deliver-order'),
    path('search-products/', search_products, name='search-products'),
    path('get-top-rated-products-by-category/', get_top_rated_product_by_category,
         name='get-top-rated-products-by-category'),
    path('generate-top-selling-products-by-category/', generate_top_selling_products_by_category,
         name='generate-top-selling-products-by-category')
]
