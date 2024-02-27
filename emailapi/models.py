from django.db import models

# Create your models here.
class APISendMailModel(models.Model):
    pass


class Employee(models.Model):
    id=models.CharField(primary_key=True,max_length=10)
    name=models.CharField(max_length=100)
    email=models.EmailField()
    address=models.CharField(max_length=150)
    phoneno=models.IntegerField()