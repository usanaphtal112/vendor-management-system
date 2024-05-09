from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from vendor.models import Vendor, PurchaseOrder, HistoricalPerformance


class DatabaseTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testusername",
            email="testemail@gmail.com",
            password="secretpassword",
        )

        # Create multiple Vendor instances
        cls.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Mumbai India",
            vendor_code="VND-2405100001",
            on_time_delivery_rate=98.0,
            quality_rating_avg=10.0,
            average_response_time=120.45,
            fulfillment_rate=50.0,
        )

        cls.historical_perfomance = HistoricalPerformance.objects.create(
            vendor=cls.vendor,
            date="2024-05-09T12:00:00Z",
            on_time_delivery_rate=50.0,
            quality_rating_avg=3.66666666,
            average_response_time=72,
            fulfillment_rate=66.66666,
        )

        # Create multiple PurchaseOrder instances for each vendor
        cls.purchase_order1 = PurchaseOrder.objects.create(
            vendor=cls.vendor,
            po_number="PO-0001",
            items={
                "items": [
                    {
                        "name": "Item 1",
                        "price": 10.99,
                        "quantity": 5,
                        "description": "Description for Item 1",
                    },
                ]
            },
            quantity=2,
            status="pending",
            quality_rating=4.0,
            order_date="2024-05-02T12:00:00Z",
            acknowledgment_date="2024-05-04T12:00:00Z",
            actual_delivery_date="2024-05-08T12:00:00Z",
            delivery_date="2024-05-12T12:00:00Z",
        )

        cls.purchase_order2 = PurchaseOrder.objects.create(
            vendor=cls.vendor,
            po_number="PO-0002",
            items={
                "items": [
                    {
                        "name": "Item 1",
                        "price": 10.99,
                        "quantity": 5,
                        "description": "Description for Item 1",
                    },
                ]
            },
            quantity=2,
            status="completed",
            quality_rating=3.5,
            order_date="2024-05-07T12:00:00Z",
            acknowledgment_date="2024-05-09T12:00:00Z",
            actual_delivery_date="2024-05-20T12:00:00Z",
            delivery_date="2024-05-25T12:00:00Z",
        )

        cls.purchase_order3 = PurchaseOrder.objects.create(
            vendor=cls.vendor,
            po_number="PO-0003",
            items={
                "items": [
                    {
                        "name": "Item 1",
                        "price": 10.99,
                        "quantity": 5,
                        "description": "Description for Item 1",
                    },
                ]
            },
            quantity=2,
            status="completed",
            quality_rating=3.5,
            order_date="2024-05-05T12:00:00Z",
            acknowledgment_date="2024-05-10T12:00:00Z",
            actual_delivery_date="2024-05-19T12:00:00Z",
            delivery_date="2024-05-17T12:00:00Z",
        )

    def test_purchase_order_model(self):
        self.assertEqual(self.purchase_order1.po_number, "PO-0001")
        self.assertEqual(self.purchase_order1.vendor.name, "Test Vendor")
        self.assertEqual(
            self.purchase_order1.items,
            {
                "items": [
                    {
                        "name": "Item 1",
                        "price": 10.99,
                        "quantity": 5,
                        "description": "Description for Item 1",
                    },
                ]
            },
        )
        self.assertEqual(self.purchase_order1.quantity, 2)
        self.assertEqual(
            self.purchase_order1.acknowledgment_date, "2024-05-04T12:00:00Z"
        )
        self.assertEqual(
            self.purchase_order1.actual_delivery_date, "2024-05-08T12:00:00Z"
        )
        self.assertEqual(self.purchase_order1.quality_rating, 4.0)
        self.assertEqual(self.purchase_order1.status, "pending")

    def test_vendor_model(self):
        self.assertEqual(self.vendor.name, "Test Vendor")
        self.assertEqual(
            self.vendor.vendor_code, "VND-2405100001"
        )  # Use today's date as created database will use today's datatime to create vendor code
        self.assertEqual(self.vendor.contact_details, "Mumbai India")
        self.assertEqual(self.vendor.on_time_delivery_rate, 98.0)
        self.assertEqual(self.vendor.quality_rating_avg, 10.0)
        self.assertEqual(self.vendor.average_response_time, 120.45)
        self.assertEqual(self.vendor.fulfillment_rate, 50.0)

    def test_historical_perfomance(self):
        self.assertEqual(self.historical_perfomance.date, "2024-05-09T12:00:00Z")
        self.assertEqual(self.historical_perfomance.on_time_delivery_rate, 50.0)
        self.assertEqual(self.historical_perfomance.quality_rating_avg, 3.66666666)
        self.assertEqual(self.historical_perfomance.average_response_time, 72)
        self.assertEqual(self.historical_perfomance.fulfillment_rate, 66.66666)
