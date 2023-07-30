from django.contrib import admin
from .models import Invoice
# Register your models here.
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('full_name_invoice', 'invoice_number',
                    'coaching_type_course_invoice', 'date_added_invoice')


admin.site.register(Invoice, InvoiceAdmin)