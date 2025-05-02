from django.contrib import admin
from BILLING.models import *

# Register your models here.
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
