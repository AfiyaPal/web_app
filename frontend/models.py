from django.db import models

# Create your models here.
class Clinic(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    contact = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name