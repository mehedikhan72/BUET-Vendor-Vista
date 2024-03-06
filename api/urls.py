from django.urls import path
from .views.auth_view import register, login
# from rest_framework_simplejwt.views import (
#     TokenRefreshView,
# )

from .views.main import add_product, get_products

urlpatterns = [
    # auth
    # path("token/", MyTokenObtainPairView.as_view()),
    # path("token/refresh/", TokenRefreshView.as_view()),

    path("register/", register, name="register"),
    path("login/", login, name="login"),

    path("add-product/", add_product, name="add-product"),
    path('products/<str:category>/', get_products, name="get-products"),
]
