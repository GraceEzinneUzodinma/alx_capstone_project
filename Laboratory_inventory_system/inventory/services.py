from django.db import transaction
from django.utils import timezone
from .models import StockBatch, StockTransaction


@transaction.atomic
def issue_stock(item, quantity, user=None, department=None):
    """
    Issues stock using FIFO (oldest batches first)
    """
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")

    total_available = item.stock_on_hand()
    if quantity > total_available:
        raise ValueError("Insufficient stock available")

    remaining = quantity

    batches = (
        StockBatch.objects
        .filter(item=item, quantity__gt=0)
        .order_by("expiry_date", "date_received")
    )

    for batch in batches:
        if remaining <= 0:
            break

        if batch.quantity >= remaining:
            batch.quantity -= remaining
            batch.save()
            remaining = 0
        else:
            remaining -= batch.quantity
            batch.quantity = 0
            batch.save()

    # Record stock transaction
    StockTransaction.objects.create(
        item=item,
        quantity=-quantity,
        transaction_type="OUT",
        department=department,
        user=user,
        created_at=timezone.now()
    )

    return True


@transaction.atomic
def receive_stock(
    item,
    quantity,
    batch_number,
    expiry_date,
    user=None
):
    """
    Receives stock into inventory
    """
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")

    # Create new batch
    StockBatch.objects.create(
        item=item,
        batch_number=batch_number,
        quantity=quantity,
        expiry_date=expiry_date
    )

    # Log transaction
    StockTransaction.objects.create(
        item=item,
        quantity=quantity,
        transaction_type="IN",
        user=user,
        created_at=timezone.now()
    )

    return True
