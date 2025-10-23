from django.contrib.auth.models import AbstractUser
from django.db import models

# class Department(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True)

#     def __str__(self):
#         return self.name 
    

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.username
