from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


# ✓ Create user

# user class ✓ Each user should have an email, name, and mobile number.
"""
User :email, name, mobile number, password, token, id, 
expense: user(many-to-many), amount, division,timestamp

"""






class CustomUser(AbstractUser):

    def __str__(self):
        return self.username


# User Model


class User(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True
    )  # One-to-One relationship with the user model
    email = models.EmailField(
        max_length=40, unique=True
    )  # String field for the student's roll number
    def __str__(self):
        return self.user.username



"""
expense: user(many-to-many), amount, division,timestamp
"""
class Expense(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.ManyToManyField(
        User
    )  # one-to-One relationship with the user model
    details=models.TextField(null=False)
    datetime=models.DateTimeField(auto_now_add=True)
    split_method=models.TextField(null=False)

    

    
