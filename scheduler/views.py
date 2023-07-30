"""
>> LOGIC FOR SCHEDULE A CLIENT 
"""

import datetime
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from clientsapp.models import Clients
from django.db.models import Q
from scheduler.models import ScheduleClients
from .forms import ScheduleForm
import openpyxl
from django.http import HttpResponse

# Schedule a client 
@login_required(login_url='loginPage')
def schedule_client(request):
    page = "Schedule clients | Edify Lab's Business Tool"
    auth_user = request.user.first_name
    all_schedule = ScheduleClients.objects.all()
    if request.method == "GET":
        all_schedule = ScheduleClients.objects.all()
        form = ScheduleForm()
        context_schedule_list = {
            "schedule_list": all_schedule, "auth_user": auth_user , "page":page}
        return render(request, "scheduler_template/schedule.html/", context_schedule_list)
    else:
        print("--------------" , request.user.first_name)
        form = ScheduleForm(request.POST)
        if form.is_valid():
            print("---valid-----")
            form.save()
    context_schedule_list = {
        "schedule_list": all_schedule, "auth_user": auth_user, "ScheduleForm": form , "page":page}
    return render(request, "scheduler_template/schedule.html/", context_schedule_list)

# Edit already scheduled client
@login_required(login_url='loginPage')
def edit_schedule(request, id):
    page = "Edit schedule client | Edify Lab's Business Tool"
    auth_user = request.user.first_name
    print(id)
    schedule = ScheduleClients.objects.get(id=id)
    if request.method == "POST":
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect("all_scheduled_clients")
    else:
        form = ScheduleForm(instance=schedule) # pass existing schedule object to the form
    context = {
        "ScheduleForm": form, # use 'form' instead of 'ScheduleForm'
        "schedule": schedule,
        "page":page
    }
    return render(request, "scheduler_template/edit_scheduled_client.html", context)

# SEARCH A CLIENT BEFORE TO SCHEDULE IT - IF NOT THEN SHOW ADD ELSE SHOW FORM
@login_required(login_url='loginPage')
def search_client_schedule(request):
    page = "Schedule form clients | Edify Lab's Business Tool"
    auth_user = request.user.first_name
    if request.method == "POST":
        title = request.POST["title"]

        lookups = Q(first_name__icontains=title) | Q(
            coaching_type_course__title__icontains=title) | Q(last_name__icontains=title)
        filter_title = Clients.objects.filter(lookups)

        print(len(filter_title), lookups)
        if title != '' and title is not None and len(filter_title) != 0:
            form = ScheduleForm()
            context_clients_list = {
                "clients_list": Clients.objects.all(), "filter_title": filter_title, "ScheduleForm": form , "page":page , "auth_user":auth_user}
        else:
            error = "NO MATCH FOUND"
            print(error)
            context_clients_list = {"error": error , "page":page , "auth_user":auth_user}
        return render(request, "scheduler_template/schedule.html/", context_clients_list)
    else:
        print("SOMETHING WENT WRONG IN SEARCH CLIENT")
        return redirect('/home/')

@login_required(login_url='loginPage')
def schedule_add(request):
    print("SCHEDULE ADD")
    page = "Schedule form | Edify Lab's Business Tool"
    if request.method == "GET":
        auth_user = request.user.first_name
        form = ScheduleForm()
    else:
        form = ScheduleForm(request.POST)
        if form.is_valid():
            # Get form data
            first_name = form.cleaned_data['first_name_S']
            last_name = form.cleaned_data['last_name_S']
            coaching_type_course = form.cleaned_data['coaching_type_course']

            # Check if a client with the same first name, last name, and coaching type course exists
            try:
                existing_client = ScheduleClients.objects.filter(first_name_S=first_name, last_name_S=last_name, coaching_type_course=coaching_type_course).latest('id')
            except ScheduleClients.DoesNotExist:
                existing_client = None

            if existing_client:
                print("INSIDE IF")
                # Increment the count for the existing client and create a new client with the entered time and sessions values
                new_client = ScheduleClients(
                    first_name_S=first_name,
                    last_name_S=last_name,
                    coaching_type_course=coaching_type_course,
                    review_call=existing_client.review_call,
                    sessions=form.cleaned_data['sessions'],  # Use the entered sessions value from the form
                    my_time_field=form.cleaned_data['my_time_field'],  # Use the entered time value from the form
                    client_count=existing_client.client_count + 1
                )

                new_client.save()
            else:
                # Create a new client with a count of 1
                new_client = form.save(commit=False)
                new_client.client_count = 1
                print("ELSE", new_client.client_count)
                new_client.save()

            return redirect("all_scheduled_clients")

    context = {
        "form": form,
        "page":page
    }
    return render(request, "scheduler_template/schedule.html", context)

# SHOW ALL ALREADY SCHEDULED CLIENTS
@login_required(login_url='loginPage')
def all_scheduled_clients(request):
    page = "All Schedule clients | Edify Lab's Business Tool"
    auth_user = request.user.first_name
    if request.method == "GET":
        all_schedule = ScheduleClients.objects.all()

        context_schedule_clients_list = {
            "schedule_list": all_schedule, "auth_user": auth_user , "page":page }
        return render(request, "scheduler_template/scheduled_clients.html", context_schedule_clients_list)
    else:
        print("------------ITS POST --------------")
        title = request.POST["title"]

        lookups = Q(first_name_S__icontains=title) | Q(
            coaching_type_course__title__icontains=title) | Q(last_name_S__icontains=title) | Q(sessions__icontains=title)
        filter_title = ScheduleClients.objects.filter(lookups)
        print("-----------",filter_title)

        if title == '' or title is  None or len(filter_title) == 0:
            error = "NO RESULTS FOUND"
            print(error)
            context_schedule_clients_list = {
            "schedule_list_filtered": filter_title, "auth_user": auth_user , "error":error , "page":page}
        else:
            context_schedule_clients_list = {"schedule_list_filtered": filter_title, "auth_user": auth_user , "page":page}
        return render(request, "scheduler_template/scheduled_clients.html", context_schedule_clients_list)

# DOWNLOAD TO PDF
@login_required(login_url='loginPage')
def download_scheduled_client(request, id):
    if request.method == "GET":
        auth_user = request.user.first_name
        client = ScheduleClients.objects.get(pk=id)
        name = client.first_name_S  # Assuming the name field exists in the ScheduleClients model
        filtered_clients = ScheduleClients.objects.filter(first_name_S=name)
        print("THIS IS THE NAEM :" , filtered_clients)
        sessions_print = filtered_clients.values_list('sessions', flat=True)
        session_end_print = filtered_clients.values_list('my_time_field', flat=True)
        print(sessions_print , session_end_print)
        
        session_times = []
            
        for session, end_time in zip(sessions_print, session_end_print):
            session_start = session.strftime("%Y-%m-%d %H:%M") if isinstance(session, datetime.datetime) else session
            session_end = end_time.strftime("%I:%M %p") if isinstance(end_time, datetime.time) else end_time
   
            session_times.append(f"Session start - <strong>{session_start}</strong>   ->  Session end - <strong>{session_end}</strong>")
            
        print("--",session_times)
        now = datetime.datetime.now
        context = {"auth_user": auth_user,
                   "page": f"EdifyLabs | download - {client.first_name_S}-{client.last_name_S}-{client.id}", "clients": client, "DT": now , "session_times": session_times,}
        return render(request, "scheduler_template/download_scheduled_client.html", context)
    
# DELETE A SELECTED CLIENT
@login_required(login_url='loginPage')
def scheduled_clients_delete(request):
    if request.method == 'POST':
        item_ids = request.POST.getlist('scheduled_clients_delete')
        print(item_ids)
        print(item_ids , "selected")
        if item_ids:
            ScheduleClients.objects.filter(id__in=item_ids).delete()
    return redirect('/all_scheduled_clients')

# DOWNLOAD TO EXCEL
def download_scheduled_clients_excel(request):
    scheduled_clients = ScheduleClients.objects.all()

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    header_row = ["ID", "First Name", "Last Name", "Course", "Review call", "Sessions start" , "Sessions ends", "count"]
    sheet.append(header_row)

    for sc_clients in scheduled_clients:
        data_row = [f"CL-{sc_clients.id}", sc_clients.first_name_S, sc_clients.last_name_S, str(sc_clients.coaching_type_course), sc_clients.review_call, sc_clients.sessions,sc_clients.my_time_field , sc_clients.client_count ]
        sheet.append(data_row)
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=Scheduled_clients_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx'

    workbook.save(response)
    
    return response