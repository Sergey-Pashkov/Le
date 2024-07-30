from django.db import models

# Create your models here.
# models.py
from django.db import models
from django.contrib.auth.models import User

class Functions_of_performers(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='functions_of_performers')

    def __str__(self):
        return self.name
