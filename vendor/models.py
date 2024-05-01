from django.db import models
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
import uuid


class Vendor(models.Model):
    name = models.CharField(max_length=225)
    contact_details = models.TextField()
    vendor_code = models.CharField(max_length=15, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Generate a unique vendor code with a prefix
        now = datetime.now()
        formatted_date = now.strftime("%y%m%d")  # Use yy for year (2 digits)
        prefix = "VND-"  # You can customize the prefix
        try:
            latest_vendor = Vendor.objects.latest("id")
            # Use latest vendor ID for code generation if exists
            self.vendor_code = f"{prefix}{formatted_date}{latest_vendor.pk + 1:0>4}"
        except Vendor.DoesNotExist:
            # If no vendors exist, start the code from 1
            self.vendor_code = f"{prefix}{formatted_date}{1:0>4}"
        super().save(*args, **kwargs)


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ]
    po_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="purchase_orders"
    )
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(default=timezone.now() + timedelta(days=7))
    # actual_delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.po_number}"


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="historical_performance"
    )
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor} - {self.date}"
