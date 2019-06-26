from django.db import models
from django.urls import reverse

# Create your models here.

class Source(models.Model):
    name = models.CharField(max_length=1000)

    def get_absolute_url(self):
        return reverse('modis:source_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=1000)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('modis:product_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

class DataSet(models.Model):
    index = models.IntegerField()
    name = models.CharField(max_length=1000)
    data_type = models.CharField(max_length=1000)
    dimensions = models.IntegerField()
    fill_value = models.IntegerField()
    valid_range = models.IntegerField()
    cell_area = models.DecimalField(decimal_places=7, max_digits=9, blank=True, null=True)

    # description = models.CharField(max_length=1000)
    # units = models.CharField(max_length=1000)
    # fill_value = models.CharField(max_length=1000)
    # valid_range = models.CharField(max_length=1000)
    # scaling_factor = models.CharField(max_length=1000)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # source = models.ForeignKey(Product.source, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('modis:dataset_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

class Span(models.Model):
    name = models.CharField(max_length=1000)

    def get_absolute_url(self):
        return reverse('modis:span_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name