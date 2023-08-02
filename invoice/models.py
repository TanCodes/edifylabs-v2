import datetime
from django.db import models
from clientsapp.models import Course
from decimal import Decimal
# Create your models here.

class Invoice(models.Model):
    full_name_invoice = models.CharField(max_length=100)
    address_invoice = models.TextField(max_length=150, blank=True)
    GST_invoice = models.CharField(max_length=100 , blank=True)
    invoice_number = models.CharField(max_length=100 , blank=True) #auto
    date_added_invoice = models.DateField(auto_now_add=True ) #auto
    coaching_type_course_invoice = models.ForeignKey(Course, on_delete=models.CASCADE)
    particular_invoice = models.TextField(blank=True)
    amount_invoice  = models.DecimalField(max_digits=20 ,decimal_places=2)
    any_discount_invoice = models.DecimalField(max_digits=20 , decimal_places=2 ,default= 0 ,blank=True)
    total_amount_invoice =  models.DecimalField(max_digits=20 , decimal_places=2 ,default= 0)
    cgst = models.PositiveIntegerField(default=9)
    sgst = models.PositiveIntegerField(default=9)
    igst = models.PositiveIntegerField(default=0)
    cgst_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    sgst_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    igst_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_amount_payable_invoice =  models.DecimalField(max_digits=20 , decimal_places=2 ,default= 0)

    def save(self, *args, **kwargs):
        # Format date_added_invoice before saving
        current_date = datetime.datetime.now()
        self.date_added_invoice = current_date.strftime('%d-%b-%y')
        
        self.total_amount_invoice = self.amount_invoice - self.any_discount_invoice
        
        if self.igst > 0:
            # If IGST is applicable
            igst_percentage = Decimal(self.igst / 100)
            self.igst_amount = igst_percentage * Decimal(self.total_amount_invoice)
            self.cgst_amount = Decimal(0)
            self.sgst_amount = Decimal(0)
            print("--IGST" ,self.igst_amount )
        else:
            # If CGST and SGST are applicable
            cgst_percentage = Decimal(self.cgst / 100)
            sgst_percentage = Decimal(self.sgst / 100)
            self.cgst_amount = cgst_percentage * Decimal(self.total_amount_invoice)
            self.sgst_amount = sgst_percentage * Decimal(self.total_amount_invoice)
            self.igst_amount = Decimal(0)
            print("--sgst" ,self.sgst_amount )
            print("--cgst" ,self.cgst_amount )
        self.total_amount_payable_invoice = self.total_amount_invoice + self.cgst_amount + self.sgst_amount + self.igst_amount
        
        # Storing invoice number as year/month/count
        if not self.id:
            self.date_added_invoice = current_date.strftime('%d-%b-%y')
            
            # Get the highest existing invoice number
            highest_invoice = Invoice.objects.order_by('-invoice_number').first()
            if highest_invoice:
                highest_invoice_number = highest_invoice.invoice_number
            else:
                highest_invoice_number = None

            # Calculate the new invoice number
            if highest_invoice_number:
                parts = highest_invoice_number.split('/')
                year, month, count = parts[0], parts[1], parts[2]
                print(f"{year} {month} {count}")

                if year == current_date.strftime('%y') and month == current_date.strftime('%m').lstrip('0'):
                    count = str(int(count) + 1)
                else:
                    count = '1'
            else:
                count = '1'
            
            year = current_date.strftime('%y')
            month = current_date.strftime('%m').lstrip('0')
            self.invoice_number = f"{year}/{month}/{count}"

        super(Invoice, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name_invoice} {self.invoice_number} ({self.date_added_invoice})"
    
    class Meta:
        ordering = ('-date_added_invoice', )
