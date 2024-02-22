from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class RelevantUserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pfp = models.ImageField(
        upload_to="profile_pictures", blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    student_id = models.CharField(max_length=100, blank=True, null=True)
    hall = models.CharField(max_length=100, blank=True, null=True)
    is_mod = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


CATEGORIES = (
    ("Clothing", "clothing"),
    ("Electronics", "electronics"),
    ("Books", "books"),
    ("Stationery", "stationery"),
    ("Accessories", "accessories"),
    ("Creative Arts", "creative_arts"),
    ("Miscellaneous", "miscellaneous"),
)


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    # TODO: figure out why this field was in ERD.
    status = models.BooleanField(default=True)

    multiple_products = models.BooleanField(default=False)
    used = models.BooleanField(default=False)
    category = models.CharField(max_length=100, choices=CATEGORIES)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # analytics
    total_sold = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name


# each product must have at least one, first one is the preview image
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="product_images", blank=True, null=True)
    
    def __str__(self):
        return self.product.name


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.product.name} - {self.size}"


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.product.name} - {self.color}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # 1 to 5
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.product.name} - {self.user.first_name} {self.user.last_name}"


class QnA(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.product.name} - {self.user.first_name} {self.user.last_name}"


class Report(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.user.first_name} {self.user.last_name}"
