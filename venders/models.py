from django.db import models
from django.db.models import Avg,Count,F
from rest_framework import status

# Create your models here.
class VenderModel(models.Model):
    name=models.CharField(max_length=100)
    contact_details=models.TextField()
    address=models.TextField()
    vender_code=models.CharField(max_length=100,unique=True)
    on_time_delivery_rate=models.FloatField(default=0)
    quality_rating_avg=models.FloatField(default=0)
    average_response_time=models.FloatField(default=0)
    fulfillment_rate=models.FloatField(default=0)

    def __str__(self):
        return self.name
    
    def claculate_on_time_delivery_rate(self):
        total_completed_pos=self.purchseorder_set.filter(status='completed').count()
        if total_completed_pos>0:
            on_time_pos=self.purchaseorder_set.filter(status='completed', 
            delivery_date__lte=F('acknowledgment_date')).count()
            self.on_time_delivery_rate=(on_time_pos/total_completed_pos)*100
            self.save()

    def claculate_quality_rating_avg(self):
        avg_rating=self.purchaseorder_set.filter(status='complted').aggregate(average_rating=Avg('quality_rating'))
        if avg_rating['average_rating']:
            self.quality_rating_avg=avg_rating['average_rating']
            self.save()
    def claculate_averange_response_time(self):
        avg_response_time=self.purchaseorder_set.filter(status='completed').aggregate(average_response=Avg(F('acknowledgment_date') - F('issue_date')))
        if avg_response_time['average_response']:
            self.average_response_time=avg_response_time['average_response'].toatal_seconds()/60
            self.save()
    def calculate_fulfillment_rate(self):
        total_pos=self.purchase_set.count()
        if total_pos>0:
            successfully_fulfilled_pos=self.purchaseorder_set.filter(status='completed').count()
            self.fulfillment_rate=(successfully_fulfilled_pos/total_pos)*100
            self.save()

class PurchaseOrderModel(models.Model):
    po_number=models.CharField(max_length=50,unique=True)
    vender=models.ForeignKey(VenderModel,on_delete=models.CASCADE)
    order_date=models.DateTimeField()
    delivery_date=models.DateTimeField()
    items=models.JSONField()
    quantity=models.IntegerField()
    status=models.CharField(max_length=20, choices=[
        ('pending','Pending'),
        ('completed','Completed'),
        ('canceled','Canceld')
    ])
    quality_rating=models.FloatField(null=True,blank=True)
    issue_date=models.DateTimeField()
    acknowledgment_date=models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.po_number

class HistoricalPerformanceModel(models.Model):
    vender=models.ForeignKey(VenderModel,on_delete=models.CASCADE)
    date=models.DateTimeField()
    on_time_delivery_rate=models.FloatField()
    quality_rating_avg=models.FloatField()
    average_response_time=models.FloatField()
    fulfillment_rate=models.FloatField()

    