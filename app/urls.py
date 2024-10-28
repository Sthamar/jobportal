from django.urls import path
from app import views




urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_list, name='search'),
    path('job/<slug:slug>', views.detail_page, name='detail_page')
]
