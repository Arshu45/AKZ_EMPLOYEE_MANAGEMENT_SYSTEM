from django.db import models

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=100, null = False)

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    salary = models.IntegerField(null=False)
    bonus = models.IntegerField(default=0)
    phone = models.IntegerField(null=False)
    location = models.CharField(max_length=100)  # Temporary default
    hire_date = models.DateField(null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"