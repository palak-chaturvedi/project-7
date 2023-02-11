from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.symbol



class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    shares = models.PositiveIntegerField()
    cost_basis = models.DecimalField(max_digits=10, decimal_places=2)
    cash = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.user}'s portfolio: {self.stock} ({self.shares} shares)"


class Trade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    shares = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.stock} - {self.shares} - {self.date}"
