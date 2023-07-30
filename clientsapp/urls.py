"""
>> URLS -> CLIENTS
"""

from django.urls import path
from clientsapp.views import home, clients_list, search_client, item_delete, download_client , download_clients_excel

urlpatterns = [
    path("home/", home, name="home"),
    path("home/<int:id>/", home, name="client_update"),
    path('clients-list/', clients_list, name='clients_list'),
    path('search-client/', search_client, name='search_client'),
    path('item_delete/', item_delete, name='item_delete'),
    path('download-client/id=<int:id>/', download_client, name='download_client'),
    path('download-clients-excel/', download_clients_excel, name='download_clients_excel'),
]
