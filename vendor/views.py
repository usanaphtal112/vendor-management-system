from rest_framework import generics, status
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import VendorPerformanceSerializer
from datetime import datetime


class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


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
