from django.db import models
from django.utils import timezone
from datetime import timedelta
from datetime import datetime


class Vendor(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=225)
    contact_details = models.TextField()
    vendor_code = models.CharField(max_length=15, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.name} -{self.vendor_id}- {self.vendor_code}"

    def save(self, *args, **kwargs):
        # Generate a unique vendor code with a prefix
        now = datetime.now()
        formatted_date = now.strftime("%y%m%d")
        prefix = "VND-"
        try:
            latest_vendor = Vendor.objects.latest("vendor_code")

            latest_numeric_part = int(latest_vendor.vendor_code.split("-")[1][6:])
            new_numeric_part = latest_numeric_part + 1
            self.vendor_code = f"{prefix}{formatted_date}{new_numeric_part:0>4}"
        except Vendor.DoesNotExist:
            self.vendor_code = f"{prefix}{formatted_date}0001"
        super().save(*args, **kwargs)


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ]
    po_id = models.AutoField(primary_key=True)
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="purchase_orders"
    )
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(default=timezone.now() + timedelta(days=7))
    actual_delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.PositiveIntegerField()
    status = status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(default=timezone.now)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.vendor} - {self.po_number}"

    def save(self, *args, **kwargs):
        if not self.po_number:
            try:
                latest_order = PurchaseOrder.objects.latest("po_id")
                latest_po_number = int(
                    latest_order.po_number.split("-")[-1]
                )  # Extract the sequential part
                new_po_number = latest_po_number + 1
            except PurchaseOrder.DoesNotExist:
                new_po_number = 1
            self.po_number = f"PO-{new_po_number:06}"
        super().save(*args, **kwargs)


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
