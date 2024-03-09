from django.urls import path
from .views.auth_view import register, login
# from rest_framework_simplejwt.views import (
#     TokenRefreshView,
# )

from .views.main import (add_product, get_products, add_product_color, add_product_size,
                         add_product_image, place_order, update_product_quantity, add_review, ask_question,
                         add_answer, add_report, get_top_selling_products)

from .views.analytics import (get_total_sales_for_each_product)

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
         name="get-top-selling-products")
]
