from django.test import TestCase
from datetime import datetime
from vendor.models import Vendor, PurchaseOrder, HistoricalPerformance


class SignalTests(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Mumbai India",
            vendor_code="VND-2405100001",
            on_time_delivery_rate=98.0,
            quality_rating_avg=10.0,
            average_response_time=120.45,
            fulfillment_rate=50.0,
        )
        self.purchase_order = PurchaseOrder.objects.create(
            vendor=self.vendor,
            po_number="PO-00010",
            items={
                "items": [
                    {
                        "name": "Item 1",
                        "price": 10.99,
                        "quantity": 5,
                        "description": "Description for Item 1",
                    }
                ]
            },
            quantity=2,
            status="pending",
            quality_rating=4.0,
            order_date="2024-05-09T12:00:00Z",
            issue_date=datetime.strptime("2024-05-09T12:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
            acknowledgment_date="2024-05-10T12:00:00Z",
            actual_delivery_date="2024-05-17T12:00:00Z",
            delivery_date="2024-05-18T12:00:00Z",
        )

    def test_update_vendor_performance(self):
        """Simulate a change in the PurchaseOrder status to 'completed'"""
        self.purchase_order.status = "completed"
        self.purchase_order.save()

        updated_vendor = Vendor.objects.get(pk=self.vendor.vendor_id)

        # Verify if the Vendor attributes have been updated
        self.assertAlmostEqual(updated_vendor.on_time_delivery_rate, 100.0)
        self.assertAlmostEqual(updated_vendor.quality_rating_avg, 4.0)
        self.assertAlmostEqual(updated_vendor.average_response_time, 24.0)
        self.assertAlmostEqual(updated_vendor.fulfillment_rate, 100.0)

        # Verify if the HistoricalPerformance object has been created or updated
        historical_performance = HistoricalPerformance.objects.get(vendor=self.vendor)
        self.assertAlmostEqual(historical_performance.on_time_delivery_rate, 100.0)
        self.assertAlmostEqual(historical_performance.quality_rating_avg, 4.0)
        self.assertAlmostEqual(historical_performance.average_response_time, 24.0)
        self.assertAlmostEqual(historical_performance.fulfillment_rate, 100.0)
