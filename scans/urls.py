from django.urls import path

from . import views

urlpatterns = [
    path('newscan', views.new_scan, name='new_scan'),
    path('triggerscan', views.trigger_scan, name='trigger_scan'),
]