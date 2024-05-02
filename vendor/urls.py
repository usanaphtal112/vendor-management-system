from django.urls import path
from .views import (
    VendorListCreateAPIView,
    VendorRetrieveUpdateDestroyAPIView,
    PurchaseOrderListCreateAPIView,
    PurchaseOrderRetrieveUpdateDestroyAPIView,
    VendorPerformanceView,
    AcknowledgePurchaseOrderView,
)

urlpatterns = [
    path(
        "vendors/",
        VendorListCreateAPIView.as_view(),
        name="vendor-list-create",
    ),
    path(
        "vendors/<int:pk>/",
        VendorRetrieveUpdateDestroyAPIView.as_view(),
        name="vendor-detail",
    ),
    path(
        "purchase_orders/",
        PurchaseOrderListCreateAPIView.as_view(),
        name="purchaseorder-list-create",
    ),
    path(
        "purchase_orders/<int:pk>/",
        PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(),
        name="purchaseorder-detail",
    ),
    path(
        "vendors/<int:vendor_id>/performance/",
        VendorPerformanceView.as_view(),
        name="vendor-performance-metrics",
    ),
    path(
        "purchase_orders/<int:po_id>/acknowledge/",
        AcknowledgePurchaseOrderView.as_view(),
        name="purchase-order-acknowledgment",
    ),
]
