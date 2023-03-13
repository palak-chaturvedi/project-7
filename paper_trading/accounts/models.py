from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User


class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, name, email, phone_number, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not name:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone_number=phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, phone_number, password):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
            phone_number=phone_number
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50,default=0)
    email = models.EmailField(max_length=100, unique=True)
    stock = models.CharField(max_length=50, default="")
    stock_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # shares = models.PositiveIntegerField()
    # cost_basis = models.DecimalField(max_digits=10, decimal_places=2)
    cash = models.DecimalField(max_digits=10, decimal_places=2, default=10)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
