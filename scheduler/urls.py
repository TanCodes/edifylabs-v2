
from django.contrib import admin
from django.urls import path
from scheduler.views import schedule_client, search_client_schedule, schedule_add, all_scheduled_clients , download_scheduled_client , scheduled_clients_delete , edit_schedule , download_scheduled_clients_excel

urlpatterns = [
    # related schedule
    path('schedule-clients/', schedule_client, name='schedule_client'),
    path('search_client_schedule/', search_client_schedule,
         name='search_client_schedule'),
    path('schedule_add', schedule_add, name='schedule_add'),
    path('all_scheduled_clients', all_scheduled_clients,
         name='all_scheduled_clients'),
    path('download-scheduled-client/id=<int:id>/', download_scheduled_client, name='download_scheduled_client'),
    path('scheduled_clients_delete/', scheduled_clients_delete, name='scheduled_clients_delete'),
    path('edit_schedule/<int:id>/', edit_schedule, name='edit_schedule'),
    path('download-scheduled-clients-excel/', download_scheduled_clients_excel, name='download_scheduled_clients_excel'),
]
