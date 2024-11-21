from django.urls import path

from account import views


urlpatterns = [
    path('login', views.login_view, name='login_view'),
    path('', views.register, name='register'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('logout/', views.logoutuser, name='logoutuser')
]
