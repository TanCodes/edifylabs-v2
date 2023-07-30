
from django.contrib import admin
from django.urls import path
from myapp.views import signup, LoginPage, logoutPage, ourstory

urlpatterns = [
    # related authentication
    path("", LoginPage, name="loginPage"),
    path("signup/", signup, name="signup"),
    # path("home/", home, name="home"),
    path("logout/", logoutPage, name="logout"),

    path("ourstory/", ourstory, name='ourstory'),

]
