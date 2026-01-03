from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    stock_on_hand = serializers.SerializerMethodField()
    minimum_stock = serializers.SerializerMethodField()
    reorder_quantity = serializers.SerializerMethodField()
    optimized_order_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            "id",
            "name",
            "category",
            "unit",
            "monthly_consumption",
            "stock_on_hand",
            "minimum_stock",
            "reorder_quantity",
            "optimized_order_quantity",
        ]

    def get_stock_on_hand(self, obj):
        return obj.stock_on_hand()

    def get_minimum_stock(self, obj):
        return obj.minimum_stock()

    def get_reorder_quantity(self, obj):
        return obj.reorder_quantity()

    def get_optimized_order_quantity(self, obj):
        return obj.optimized_order_quantity()
