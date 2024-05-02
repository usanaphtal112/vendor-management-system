from rest_framework import generics, status
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import VendorPerformanceSerializer
from datetime import datetime
from drf_spectacular.utils import extend_schema


@extend_schema(
    description="List and create a new Vendors",
    tags=["Vendor"],
)
class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


@extend_schema(
    description="View details, Update and delete vendor",
    tags=["Vendor"],
)
class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = "vendor_id"


@extend_schema(
    description="List and create a new Purchase Order",
    tags=["Purchase Order"],
)
class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


@extend_schema(
    description="View details, Update and delete Purchase Order",
    tags=["Purchase Order"],
)
class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


@extend_schema(
    description="List Vendor perfomance",
    tags=["Vendor"],
)
class VendorPerformanceView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            serializer = VendorPerformanceSerializer(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response(
                {"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND
            )


@extend_schema(
    description="Acknownoldge the Order",
    tags=["Purchase Order"],
)
class AcknowledgePurchaseOrderView(APIView):
    def post(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
            # Check if the purchase order has already been acknowledged
            if purchase_order.acknowledgment_date is not None:
                return Response(
                    {"error": "Purchase order already acknowledged"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Update acknowledgment_date to current timestamp
            purchase_order.acknowledgment_date = datetime.now()
            purchase_order.save()

            # Trigger recalculation of average_response_time
            # This logic should ideally be handled by signals

            return Response(
                {"message": "Purchase order acknowledged successfully"},
                status=status.HTTP_200_OK,
            )
        except PurchaseOrder.DoesNotExist:
            return Response(
                {"error": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND
            )
