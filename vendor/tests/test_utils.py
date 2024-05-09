from django.test import TestCase
from vendor.models import PurchaseOrder
from .test_models import DatabaseTest
from django.db.models import Avg, F
from vendor.utils import (
    calculate_on_time_delivery_rate,
    calculate_quality_rating_average,
    calculate_average_response_time,
    calculate_fulfillment_rate,
)


class UtilsTests(TestCase):
    @classmethod
    def setUp(cls):
        """Create a Vendor instance"""
        super().setUpClass()
        cls.vendor = DatabaseTest.vendor

    def test_calculate_on_time_delivery_rate(self):
        """Test logic for calculating on-time delivery rate"""
        completed_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor, status="completed"
        )
        total_completed_orders = completed_orders.count()
        on_time_orders = completed_orders.filter(
            actual_delivery_date__lte=F("delivery_date")
        ).count()
        expected_rate = (
            (on_time_orders / total_completed_orders) * 100
            if total_completed_orders > 0
            else 0.0
        )
        result = calculate_on_time_delivery_rate(self.vendor)

        self.assertEqual(result, expected_rate)

    def test_calculate_quality_rating_average(self):
        """Test logic for calculating quality rating average"""
        expected_average = (
            PurchaseOrder.objects.filter(
                vendor=self.vendor, quality_rating__isnull=False, status="completed"
            ).aggregate(avg_rating=Avg("quality_rating"))["avg_rating"]
            or 0
        )

        result = calculate_quality_rating_average(self.vendor)
        self.assertEqual(result, expected_average)

    def test_calculate_average_response_time(self):
        """Test logic for calculating average response time"""
        all_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor, acknowledgment_date__isnull=False
        )
        total_orders = all_orders.count()
        total_response_time = sum(
            (order.acknowledgment_date - order.issue_date).total_seconds()
            for order in all_orders
        )
        expected_average = (
            (total_response_time / total_orders) / 3600 if total_orders > 0 else 0.0
        )
        result = calculate_average_response_time(self.vendor)
        self.assertEqual(result, expected_average)

    def test_calculate_fulfillment_rate(self):
        """Test logic for calculating fulfillment rate"""
        total_orders = PurchaseOrder.objects.filter(vendor=self.vendor).count()
        completed_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor, status="completed"
        ).count()
        expected_fulfillment_rate = (
            (completed_orders / total_orders) * 100 if total_orders > 0 else 0.0
        )
        result = calculate_fulfillment_rate(self.vendor)
        self.assertEqual(result, expected_fulfillment_rate)
