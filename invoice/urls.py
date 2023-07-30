
from django.contrib import admin
from django.urls import path
from invoice.views import invoice_dashboard , invoice_add , invoice_display , search_invoice, invoice_item_delete, invoice , download_invoice_excel

urlpatterns = [
    path("invoice-dashboard/", invoice_dashboard, name='invoice_dashboard'),
    path('invoice_add', invoice_add, name='invoice_add'),
    path('invoice_display', invoice_display, name='invoice_display'),
    path('search_invoice/', search_invoice,name='search_invoice'),
    path('invoice_item_delete/', invoice_item_delete, name='invoice_item_delete'),
    path("invoice-download/<int:id>/", invoice, name='invoice'),
        path('download-invoice-excel/', download_invoice_excel, name='download_invoice_excel'),
]
