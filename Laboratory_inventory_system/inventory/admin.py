from django.contrib import admin
from .models import Item, StockBatch, StockTransaction

admin.site.register(Item)
admin.site.register(StockBatch)
admin.site.register(StockTransaction)

# Register your models here.
