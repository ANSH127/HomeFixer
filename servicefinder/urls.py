from django.contrib import admin
from django.urls import path,include
from servicefinder import views
urlpatterns = [
    
    path('',views.home,name="home"),
    path('<str:slug>/<str:slug2>/',views.home1,name="home1"),
    path('<str:slug>/<str:slug2>/<int:id>/checkout',views.checkout,name="checkout"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path('login/',views.handlelogin,name="login"),
    path('signup/',views.hanldesignup,name="signup"),
    path('logout/',views.handlelogout,name="logout"),
    path('partner/',views.partner,name="partner"),
    path('booking/',views.booking,name="booking"),

] 