from django.contrib import admin

# Register your models here.

from .models import Source
admin.site.register(Source)

from .models import Product
admin.site.register(Product)

from .models import DataSet
admin.site.register(DataSet)

from .models import Span
admin.site.register(Span)