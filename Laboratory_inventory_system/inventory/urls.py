from django.urls import path
from .views import inventory_dashboard, ItemListAPIView

urlpatterns = [
    path("dashboard/", inventory_dashboard, name="inventory-dashboard"),
    path("items/", ItemListAPIView.as_view(), name="api-items"),
]
