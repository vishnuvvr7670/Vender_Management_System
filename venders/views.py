from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.utils.timezone import timedelta

# Create your views here.
from venders.models import *
from venders.serializers import *
from rest_framework import viewsets

class VenderModelViewSet(viewsets.ModelViewSet):
    queryset=VenderModel.objects.all()
    serializer_class=VenderModelSerializer

@api_view(['GET'])
def get_vender_performance(request,vender_id):
    vendor=get_object_or_404(VenderModel,pk=vender_id)

    # Calculate on-time delivery rate
    total_completed_pos = vendor.purchase_orders.filter(status='completed').count()
    on_time_deliveries = vendor.purchase_orders.filter(
        status='completed', delivery_date__lte=F('acknowledgment_date')
    ).count()
    on_time_delivery_rate = (on_time_deliveries / total_completed_pos) * 100 if total_completed_pos > 0 else 0
    
    # Calculate quality rating average
    quality_rating_avg = vendor.purchase_orders.filter(
        status='completed', quality_rating__isnull=False
    ).aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating'] or 0
    
    # Calculate average response time
    avg_response_time = vendor.purchase_orders.filter(
        status='completed', acknowledgment_date__isnull=False
    ).aggregate(avg_response_time=Avg(
        F('acknowledgment_date') - F('issue_date')
    ))['avg_response_time'] or timedelta(0)
    
    # Calculate fulfillment rate
    total_pos = vendor.purchase_orders.count()
    fulfilled_pos = vendor.purchase_orders.filter(status='completed').count()
    fulfillment_rate = (fulfilled_pos / total_pos) * 100 if total_pos > 0 else 0

    performance_metrics = {
        'on_time_delivery_rate': on_time_delivery_rate,
        'quality_rating_avg': quality_rating_avg,
        'average_response_time': avg_response_time.total_seconds() / 60,  # Convert to minutes
        'fulfillment_rate': fulfillment_rate,
    }
    
    return Response(performance_metrics)

@api_view(['POST'])
def acknowledge_purchase_order(request, po_id):
    po = get_object_or_404(PurchaseOrderModel, pk=po_id)
    # Logic to update acknowledgment date
    po.acknowledgment_date = timezone.now()
    po.save()
    
    return Response({'message': 'Purchase order acknowledged successfully.'}, status=status.HTTP_200_OK)


