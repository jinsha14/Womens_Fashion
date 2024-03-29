from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.


# class Customer(models.Model):
#     GENDER_CHOICES = [
#         ('M', 'Male'),
#         ('F', 'Female'),
#         ('O', 'Other'),
#     ]
#
#     firstname = models.CharField(max_length=100)
#     lastname = models.CharField(max_length=100)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
#     phone = models.CharField(max_length=15)
#     email = models.EmailField(max_length=100)
#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)
#     confirm_password = models.CharField(max_length=100)
#     address = models.CharField(max_length=100)
#     country = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     pin = models.CharField(max_length=10)
#
#     def __str__(self):
#         return self.username


class UserProfile(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.EmailField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.firstname


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='product_images/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    size = models.CharField(max_length=20, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def calculate_total(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.user.username}'s Cart - {self.product.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    shipping_address = models.TextField()
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    pincode = models.CharField(max_length=10)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return f"OrderItem - {self.product.name} ({self.quantity})"