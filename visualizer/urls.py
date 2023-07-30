
from django.contrib import admin
from django.urls import path
from visualizer.views import visualizer_home

urlpatterns = [
    path("visualizer-dashboard/", visualizer_home, name='visualizer_home'),
]
