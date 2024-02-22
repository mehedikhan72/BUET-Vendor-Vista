from django.contrib import admin
from .models import User, RelevantUserData, Product, ProductImage, ProductSize, ProductColor, Review, QnA, Report

# Register your models here.

admin.site.register(User)   
admin.site.register(RelevantUserData)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductSize)
admin.site.register(ProductColor)
admin.site.register(Review)
admin.site.register(QnA)
admin.site.register(Report)

