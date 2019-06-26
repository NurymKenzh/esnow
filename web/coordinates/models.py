from django.db import models
from django.urls import reverse

# Create your models here.

class CoordinateSystem(models.Model):
    name = models.CharField(max_length=1000)

    def get_absolute_url(self):
        return reverse('coordinates:coordinatesystem_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name