"""
>> LOGIC FUNCTIONS FOR CLIENTS 
"""

from django.shortcuts import render,  redirect
from django.contrib.auth.decorators import login_required
from clientsapp.models import Clients
from .forms import ClientForm
from django.db.models import Q
import datetime
import openpyxl
from django.http import HttpResponse
# pass - admin - 123
# pass - hruser - 123


# HOME -> FORM DISPLAY - ADD CLIENT - UPDATE CLIENT
@login_required(login_url='loginPage')
def home(request, id=0):
    if request.method == "GET":
        auth_user = request.user.first_name
        all_clients = Clients.objects.all()

        male_count = Clients.objects.filter(gender='M').count()
        female_count = Clients.objects.filter(gender='F').count()
        other_count = Clients.objects.filter(gender='O').count()
        print("Male count:", male_count)
        print(female_count)
        print(other_count)
        gender_count  = [male_count , female_count , other_count]
        gender_name = ["Male" , "Female" , "Others"]

        if id == 0:
            form = ClientForm()
        else:
            client = Clients.objects.get(pk=id)
            form = ClientForm(instance=client)
        context = {"auth_user": auth_user,
                   "page": "HOME | CLIENT | Edify Lab's Business Tool ", "ClientForm": form, "total_clients":  len(all_clients) , "gender_count" : gender_count , "gender_name" : gender_name }
        return render(request, "home.html", context)
    else:
        if id == 0:
            form = ClientForm(request.POST)
        else:
            client = Clients.objects.get(pk=id)
            form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()

        return redirect('/clients-list/')

# DISPLAYS ALL CLIENTS 
@login_required(login_url='loginPage')
def clients_list(request):
    all_clients = Clients.objects.all()
    page = "All clients | Edify Lab's Business Tool"
    if len(all_clients) != 0:
        context_clients_list = {
            "clients_list": all_clients, "total_clients": len(all_clients) , "page" : page}
    else:
        error = "NO SILENTS 0"
        context_clients_list = {"error": error  , "page":page}
    return render(request, "clients_template/clients_list.html/", context_clients_list)

# DELETE A SELECTED CLIENT
@login_required(login_url='loginPage')
def item_delete(request):
    if request.method == 'POST':
        item_ids = request.POST.getlist('item_ids')
        print(item_ids , "SELECTED")
        if item_ids:
            Clients.objects.filter(id__in=item_ids).delete()
    return redirect('/clients-list/')

# SEARCH CLIENT -> FNAME , LNAME , EMAIL , COURSE 
@login_required(login_url='loginPage')
def search_client(request):
    if request.method == "POST":
        page = "Search clients | Edify Lab's Business Tool"
        title = request.POST["title"]

        lookups = Q(first_name__icontains=title) | Q(
            coaching_type_course__title__icontains=title) | Q(last_name__icontains=title) | Q(email_id__icontains=title)
        filter_title = Clients.objects.filter(lookups)

        print(len(filter_title), lookups)
        if title != '' and title is not None and len(filter_title) != 0:

            context_clients_list = {
                "clients_list": Clients.objects.all(), "filter_title": filter_title, "filter_title_total": len(filter_title) , "page":page}
        else:
            error = "NO MATCH FOUND"
            context_clients_list = {"error": error , "page":page}
        return render(request, "clients_template/clients_list.html/", context_clients_list)
    else:
        print("---------------SOMETHING WENT WRONG IN SEARCH CLIENT-----------------------")
        return redirect('/home/')

# DOWNLOAD TO PDF
@login_required(login_url='loginPage')
def download_client(request, id):
    if request.method == "GET":
        auth_user = request.user.first_name
        client = Clients.objects.get(pk=id)
        now = datetime.datetime.now
        context = {"auth_user": auth_user,
                   "page": f"EdifyLabs | download - {client.first_name}-{client.last_name}-{client.id}", "clients": client, "DT": now}
        return render(request, "clients_template/download_client.html", context)

# DOWNLOAD TO EXCEL
def download_clients_excel(request):
    clients = Clients.objects.all()

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    header_row = ["ID", "First Name", "Last Name", "Email", "Gender", "DOB" , "Address", "Contact" , "Company" ,"Course" ]
    sheet.append(header_row)

    for client in clients:
        data_row = [f"CL-{client.id}", client.first_name, client.last_name, client.email_id, client.gender, client.date_of_birth,client.address , client.contact , client.company_name, client.coaching_type_course.title]
        sheet.append(data_row)
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=clients_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx'

    workbook.save(response)
    
    return response
