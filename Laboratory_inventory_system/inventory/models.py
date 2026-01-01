from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import math


class Item(models.Model):
    CATEGORY_CHOICES = [
        ("REAGENT", "Reagent"),
        ("CONSUMABLE", "Consumable"),
        ("PPE", "PPE"),
        ("EQUIPMENT", "Equipment"),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    unit = models.CharField(max_length=50)  # e.g. box, pack, vial
    vendor_pack_size = models.PositiveIntegerField(
        help_text="Number of units per vendor pack"
    )

    monthly_consumption = models.PositiveIntegerField(
        help_text="Average monthly usage"
    )
    lead_time_months = models.PositiveIntegerField(
        default=2,
        help_text="Lead time in months (e.g. 2, 3, or 4)"
    )
    reserve_months = models.PositiveIntegerField(
        default=1,
        help_text="Reserve buffer in months"
    )

    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def minimum_stock(self):
        return self.monthly_consumption * self.lead_time_months

    def reserve_quantity(self):
        return self.monthly_consumption * self.reserve_months

    def __str__(self):
        return self.name
    

class StockBatch(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="batches"
    )
    batch_number = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField()
    date_received = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} - Batch {self.batch_number}"

class StockTransaction(models.Model):
    TRANSACTION_TYPE = [
        ("IN", "Stock In"),
        ("OUT", "Stock Out"),
    ]

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    quantity = models.IntegerField(
        help_text="Positive for IN, negative for OUT"
    )
    transaction_type = models.CharField(
        max_length=3,
        choices=TRANSACTION_TYPE
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} ({self.transaction_type})"

    def stock_on_hand(self):
        total = 0
        for batch in self.batches.all():
            total += batch.quantity
        return total

    def quantity_to_order(self):
        required = self.minimum_stock() + self.reserve_quantity()
        to_order = required - self.stock_on_hand()
        return max(to_order, 0)

    def optimized_order_quantity(self):
        if self.vendor_pack_size == 0:
            return 0
        packs = math.ceil(self.quantity_to_order() / self.vendor_pack_size)
        return packs * self.vendor_pack_size
