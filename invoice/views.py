"""
>> LOGIC FUNCTIONS FOR INVOICE GENERATION 
"""

from django.shortcuts import redirect, render
from .models import Invoice
from .forms import InvoiceForm
from django.contrib.auth.decorators import login_required
from num2words import num2words
from django.db.models import Q
import datetime
import openpyxl
from django.http import HttpResponse

# INVOICE DASHBOARD - DISPLAY FORM
@login_required(login_url='loginPage')
def invoice_dashboard(request):
    user = request.user.first_name
    form = InvoiceForm()
    all_invoice = Invoice.objects.all()
    highest_invoice = Invoice.objects.order_by('-invoice_number').first()
    print(highest_invoice)
    context = {"page": "INVOICE | Edify Lab's Business Tool ","InvoiceForm" : form, "auth_user" :user , "total_invoice": len(all_invoice)}
    return render(request, "invoice_template/invoice_dashboard.html" , context)

# DISPLAYS ALL THE INVOICES FROM THE DB
@login_required(login_url='loginPage')
def invoice_display(request):
    all_invoice = Invoice.objects.all()
    print(all_invoice)
    if len(all_invoice) != 0:
        context_invoice_list = { "page": "ALL INVOICE | Edify Lab's Business Tool ",
            "invoice_display": all_invoice, "total_invoice": len(all_invoice)}
    else:
        error = "NO INVOICE - 0"
        context_invoice_list = {"error": error , "page": " ALL INVOICE | Edify Lab's Business Tool "}
    return render(request, "invoice_template/invoice_display.html/", context_invoice_list)

# ADD A NEW INVOICE TO THE DB FROM DASHBOARD
@login_required(login_url='loginPage')
def invoice_add(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                return redirect('invoice_display')
        except:
            print('Form is not valid')  
    else:
        form = InvoiceForm()
    return render(request, 'invoice_template/invoice_dashboard.html', {'InvoiceForm': form})

# DELETE A SELECTED INVOICE
@login_required(login_url='loginPage')
def invoice_item_delete(request):
    if request.method == 'POST':
        item_ids = request.POST.getlist('item_ids_invoice')
        print(item_ids , "seleceted")
        if item_ids:
            Invoice.objects.filter(id__in=item_ids).delete()
    return redirect('invoice_display')

# GO TO DOWNLOAD PAGE INVOICE
@login_required(login_url='loginPage')
def invoice(request, id):
    auth_user = request.user.first_name
    invoice_of_id = Invoice.objects.get(pk=id)
    payable_amount = invoice_of_id.total_amount_payable_invoice
    payable_amount_text = num2words(payable_amount, lang='en').title() + ' Only'
    payable_amount_text = payable_amount_text.replace('-', ' ').replace(',', '')
    now = datetime.datetime.now
    context = {"auth_user": auth_user,
                "title": f"EdifyLabs | invoice - {invoice_of_id.full_name_invoice}-{invoice_of_id.invoice_number}", "invoice_of_id": invoice_of_id, "payable_amount_text": payable_amount_text}
    return render(request, "invoice_template/download_invoice.html", context)

# SEARCH INVOICE
@login_required(login_url='loginPage')
def search_invoice(request):
    if request.method == "POST":
        title = request.POST["title"]

        lookups = Q(full_name_invoice__icontains=title) | Q(
            coaching_type_course_invoice__title__icontains=title) | Q(invoice_number__icontains=title) | Q(total_amount_payable_invoice__icontains=title)
        filter_title = Invoice.objects.filter(lookups)

        print(f" INVOICE {len(filter_title)}  {lookups}")
        if title != '' and title is not None and len(filter_title) != 0:

            context_invoice_list = {
                "invoice_list_all": Invoice.objects.all(), "filter_title": filter_title, "filter_title_total": len(filter_title)}
        else:
            error = "NO MATCH FOUND"
            context_invoice_list = {"error": error}
        return render(request, "invoice_template/invoice_display.html/", context_invoice_list)
    else:
        print("---------------SOMETHING WENT WRONG IN SEARCH INVOICE-----------------------")
        return redirect('/home/')


# DOWNLOAD TO EXCEL
def download_invoice_excel(request):
    invoice_all = Invoice.objects.all()

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    header_row = ["ID", "Full Name", "Address", "GST no.", "Invoice number", "Course" , "Particular detail", "Amount" , "Discount" , "Total amount" , "CGST %" , "SGST %" , "IGST %" , "CGST amount" ,"SGST amount" ,"IGST amount" , "Total amount payable"]
    sheet.append(header_row)

    for inv in invoice_all:
        data_row = [f"INV-{inv.id}", inv.full_name_invoice, inv.address_invoice, inv.GST_invoice , inv.invoice_number , str(inv.coaching_type_course_invoice), inv.particular_invoice, inv.amount_invoice,
                    inv.any_discount_invoice , inv.total_amount_invoice , inv.cgst , inv.sgst , inv.igst , inv.cgst_amount , inv.sgst_amount, inv.igst_amount , inv.total_amount_payable_invoice ]
        sheet.append(data_row)
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=invoice_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx'

    workbook.save(response)
    
    return response

# todo : add igst in invoice 18% ->international