# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model

# from django.db import models

# User = get_user_model()
class UserDetails(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    PhoneNumber = models.IntegerField()
    stock = models.CharField(max_length=50, default="")
    stock_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # shares = models.PositiveIntegerField()
    # cost_basis = models.DecimalField(max_digits=10, decimal_places=2)
    cash = models.DecimalField(max_digits=10, decimal_places=2, default=10)

    def __str__(self):
        return self.name

class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    symbol = models.CharField(max_length=10, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.symbol



# class Portfolio(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     stock = models.CharField(max_length=50,default="")
#     stock_value = models.DecimalField(max_digits=10,decimal_places=2,default=0)
#     # shares = models.PositiveIntegerField()
#     # cost_basis = models.DecimalField(max_digits=10, decimal_places=2)
#     cash = models.DecimalField(max_digits=10,decimal_places=2,default=10)
#
#     def __str__(self):
#         return f"{self.user}'s portfolio: {self.cash}"


class Trade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.CharField(max_length=50, default="")
    shares = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    type = models.CharField(max_length=4, default="null")

    def __str__(self):
        return f"{self.user} - {self.stock} - {self.shares} - {self.date}"
