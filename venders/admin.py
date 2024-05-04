from django.contrib import admin

# Register your models here.
from venders.models import *

admin.site.register(VenderModel)

admin.site.register(PurchaseOrderModel)

admin.site.register(HistoricalPerformanceModel)