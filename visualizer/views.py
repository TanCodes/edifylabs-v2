"""
>> LOGIC FUNCTIONS FOR VISUALIZATION 
"""

from django.shortcuts import render,  redirect
from django.contrib.auth.decorators import login_required
from clientsapp.models import Clients ,Course
from scheduler.models import ScheduleClients
from invoice.models import Invoice
from django.db.models import Q
from django.db.models import Count
from django.db.models.functions import ExtractMonth
import calendar
import datetime
from django.db.models import Count
from django.db.models import Sum
from django.db.models.functions import ExtractYear, ExtractMonth

@login_required(login_url='loginPage')
def visualizer_home(request):
    auth_user = request.user.first_name
    if request.method == "GET":
        # > course
        course_counts = Clients.objects.values('coaching_type_course__title').annotate(count=Count('coaching_type_course'))

        course_names = []
        counts = []
        for course in course_counts:
            course_name = course['coaching_type_course__title']
            count = course['count']
            course_names.append(course_name)
            counts.append(count)
        print(course_names, counts)
       
        all_clients = Clients.objects.all()
        all_scheduled = ScheduleClients.objects.all()
        all_invoice = Invoice.objects.all()

        #> clients - gender
        male_count = Clients.objects.filter(gender='M').count()
        female_count = Clients.objects.filter(gender='F').count()
        other_count = Clients.objects.filter(gender='O').count()
        gender_count  = [male_count , female_count , other_count]
        gender_name = ["Male" , "Female" , "Others"]

        #>total_amount_payable_invoice

        total_amounts_payable = sum(Invoice.objects.values_list('total_amount_payable_invoice', flat=True))
        import locale
        locale.setlocale(locale.LC_ALL, 'en_IN')

        total_amounts_payable = locale.format_string("%.2f ₹", total_amounts_payable, grouping=True)
        print(total_amounts_payable)

        #> Fetching the monthly count of clients added within the current year
        current_year = datetime.datetime.now().year

        monthly_counts = Clients.objects.filter(date_added__year=current_year).annotate(
            month=ExtractMonth('date_added')
        ).values('month').annotate(count=Count('id'))

        # Sorting the monthly counts based on the month
        monthly_counts = sorted(monthly_counts, key=lambda x: x['month'])

        # Extracting the month names and count values
        months = [calendar.month_name[item['month']] for item in monthly_counts]
        c_counts = [item['count'] for item in monthly_counts]

        print(months , c_counts)

        #> Fetching the monthly count of invoices generated within the current year
        monthly_invoice_counts = Invoice.objects.filter(date_added_invoice__year=current_year).annotate(
            month=ExtractMonth('date_added_invoice')
        ).values('month').annotate(count=Count('id'))

        # Sorting the monthly invoice counts based on the month
        monthly_invoice_counts = sorted(monthly_invoice_counts, key=lambda x: x['month'])

        # Extracting the month names and count values
        inv_months = [calendar.month_name[item['month']] for item in monthly_invoice_counts]
        invoice_counts_month = [item['count'] for item in monthly_invoice_counts]
        print(inv_months,invoice_counts_month)

        #> Fetching the monthly count of scheduled sessions

        session_months = []
        session_counts = []

        for session in all_scheduled:
            session_date = datetime.datetime.strptime(session.sessions, '%Y-%m-%d %H:%M')
            month_name = calendar.month_name[session_date.month]

            if month_name not in session_months:
                session_months.append(month_name)
                session_counts.append(1)
            else:
                index = session_months.index(month_name)
                session_counts[index] += 1

        print(session_months, session_counts)

        context = {"auth_user": auth_user,
                   "page": "VISUALIZATION | Edify Lab's Business Tool ", 
                   "total_clients":  len(all_clients) , 
                   "total_scheduled":  len(all_scheduled) , 
                   "total_invoices":  len(all_invoice) ,
                   "total_amounts_payable" : total_amounts_payable, 
                   "gender_count" : gender_count , "gender_name" : gender_name , 
                   "months" :months , "c_counts" : c_counts , 
                   "course_name" : course_names , "course_count" : counts, 
                   "session_months":session_months, "session_counts" :session_counts , 
                   "inv_months" :inv_months , "invoice_counts_month":invoice_counts_month}

    return render(request, "visualizer_template/visualizer_home.html", context)

