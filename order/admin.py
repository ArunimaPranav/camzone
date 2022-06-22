from django.contrib import admin

from order.models import Myorder, Order

# Register your models here.
admin.site.register(Myorder)
admin.site.register(Order)