from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, HistoricalPerformance
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

            # Update or create HistoricalPerformance instance
            (
                historical_performance,
                created,
            ) = HistoricalPerformance.objects.get_or_create(
                vendor=vendor,
                date=instance.issue_date.date(),  # Assuming date is sufficient for historical records
                defaults={
                    "on_time_delivery_rate": vendor.on_time_delivery_rate,
                    "quality_rating_avg": vendor.quality_rating_avg,
                    "average_response_time": vendor.average_response_time,
                    "fulfillment_rate": vendor.fulfillment_rate,
                },
            )
            if not created:
                # Update existing HistoricalPerformance instance
                historical_performance.on_time_delivery_rate = (
                    vendor.on_time_delivery_rate
                )
                historical_performance.quality_rating_avg = vendor.quality_rating_avg
                historical_performance.average_response_time = (
                    vendor.average_response_time
                )
                historical_performance.fulfillment_rate = vendor.fulfillment_rate
                historical_performance.save()
    except ZeroDivisionError:
        pass
