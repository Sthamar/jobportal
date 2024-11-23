from django.urls import path
from employer import views
urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create_job, name='create'),
    path('create/thankyou', views.thank, name='thank'),
    path('edit/<slug:slug>', views.edit_page, name='edit_page'),
    path('edit/<slug:slug>/delete', views.delete_job, name='delete_job'),
    path('applicants/<slug:slug>',views.applicant_list, name='applicant_list'),
    path('applicants/<slug:slug>/<int:id>', views.applicant_detail, name='applicant_detail')
]
