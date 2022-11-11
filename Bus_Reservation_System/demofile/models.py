from django.db import models

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images',null=True)
    resume = models.FileField(upload_to = 'images',null=True)


class Employee(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    salary = models.PositiveIntegerField()
    age = models.PositiveIntegerField()
    j_date = models.DateField(null=True)
    experience = models.PositiveBigIntegerField()