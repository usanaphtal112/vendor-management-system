from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder
from .utils import (
    calculate_on_time_delivery_rate,
    calculate_quality_rating_average,
    calculate_average_response_time,
    calculate_fulfillment_rate,
)


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, created, **kwargs):
    try:
        if not created:
            vendor = instance.vendor
            # On-Time Delivery Rate: Recalculate if PO status changed to 'completed'
            if instance.status == "completed":
                vendor.on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)

            # Quality Rating Average: Update if quality rating provided and PO completed
            if instance.quality_rating is not None and instance.status == "completed":
                vendor.quality_rating_avg = calculate_quality_rating_average(vendor)

            # Average Response Time: Recalculate if PO acknowledged by vendor
            if instance.acknowledgment_date is not None:
                vendor.average_response_time = calculate_average_response_time(vendor)

            # Fulfillment Rate: Recalculate on any change in PO status
            vendor.fulfillment_rate = calculate_fulfillment_rate(vendor)

            vendor.save()
    except ZeroDivisionError:
        pass
