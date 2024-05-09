from django.db.models import Avg, F, Q


def calculate_on_time_delivery_rate(vendor):
    try:
        completed_orders = vendor.purchase_orders.filter(status="completed")
        total_completed_orders = completed_orders.count()

        on_time_orders = completed_orders.filter(
            Q(status="completed") & Q(actual_delivery_date__lte=F("delivery_date"))
        ).count()

        return (on_time_orders / total_completed_orders) * 100
    except ZeroDivisionError:
        return 0


def calculate_quality_rating_average(vendor):
    try:
        return (
            vendor.purchase_orders.filter(quality_rating__isnull=False).aggregate(
                avg_rating=Avg("quality_rating")
            )["avg_rating"]
            or 0
        )
    except ZeroDivisionError:
        return 0


def calculate_average_response_time(vendor):
    try:
        all_orders = vendor.purchase_orders.filter(acknowledgment_date__isnull=False)
        total_orders = all_orders.count()
        total_response_time = sum(
            (order.acknowledgment_date - order.issue_date).total_seconds()
            for order in all_orders
        )
        return (total_response_time / total_orders) / 3600
    except ZeroDivisionError:
        return 0


def calculate_fulfillment_rate(vendor):
    try:
        total_orders = vendor.purchase_orders.count()
        fulfilled_orders = vendor.purchase_orders.filter(status="completed").count()
        return (fulfilled_orders / total_orders) * 100
    except ZeroDivisionError:
        return 0
