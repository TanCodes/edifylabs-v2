
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('admin/', admin.site.urls, name='admin'),
    path("", include("myapp.urls")),
    path("", include("clientsapp.urls")),
    path("", include("scheduler.urls")),
    path("", include("invoice.urls")),
    path("", include("visualizer.urls")),
]
