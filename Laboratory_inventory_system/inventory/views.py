from django.shortcuts import render
from .models import Item

def inventory_dashboard(request):
    items = Item.objects.all()
    return render(request, "inventory/dashboard.html", {"items": items})


from rest_framework.generics import ListAPIView
from .models import Item
from .serializers import ItemSerializer

class ItemListAPIView(ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

# Create your views here.
